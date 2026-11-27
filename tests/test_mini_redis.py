import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from mini_redis import MiniRedis, SkipList


class TestSkipList(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(SkipList().range_by_rank(0, -1), [])

    def test_order_and_rank(self):
        sl = SkipList()
        for s, m in [(85.5, "Alice"), (92.0, "Bob"), (78.0, "Charlie")]:
            sl.insert(s, m)
        self.assertEqual([m for m, _ in sl.range_by_rank(0, -1)],
                         ["Charlie", "Alice", "Bob"])
        self.assertEqual(sl.range_by_rank(1, 1), [("Alice", 85.5)])
        self.assertEqual(sl.range_by_rank(-1, -1), [("Bob", 92.0)])

    def test_update_moves_member(self):
        sl = SkipList()
        sl.insert(92.0, "Bob")
        sl.insert(99.0, "Bob")          # 更新分数，不应产生重复
        self.assertEqual(sl.range_by_rank(0, -1), [("Bob", 99.0)])

    def test_remove(self):
        sl = SkipList()
        sl.insert(1.0, "a")
        self.assertTrue(sl.remove(1.0, "a"))
        self.assertFalse(sl.remove(1.0, "a"))
        self.assertEqual(sl.range_by_rank(0, -1), [])

    def test_score_range(self):
        sl = SkipList()
        for s, m in [(1.0, "a"), (2.0, "b"), (3.0, "c")]:
            sl.insert(s, m)
        self.assertEqual(sl.range_by_score(1.5, 2.5), [("b", 2.0)])


class TestMiniRedis(unittest.TestCase):
    def _clock(self):
        box = {"t": 0.0}
        return box, (lambda: box["t"])

    def test_string_crud(self):
        r = MiniRedis()
        self.assertIsNone(r.get("missing"))
        r.set("name", "小明")
        r.set("score", 98)
        self.assertEqual(r.get("name"), "小明")
        self.assertEqual(r.get("score"), "98")
        r.delete("name")
        self.assertIsNone(r.get("name"))

    def test_expire_lazy_delete(self):
        box, clock = self._clock()
        r = MiniRedis(clock=clock)
        r.set("temp", "x")
        r.expire("temp", 2)
        self.assertEqual(r.get("temp"), "x")
        box["t"] = 3.0
        self.assertIsNone(r.get("temp"))

    def test_expire_reset_defers_deletion(self):
        box, clock = self._clock()
        r = MiniRedis(clock=clock)
        r.set("k", "v")
        r.expire("k", 2)
        r.expire("k", 10)               # 重新设置更晚的过期
        box["t"] = 3.0
        self.assertEqual(r.get("k"), "v")
        box["t"] = 11.0
        self.assertIsNone(r.get("k"))

    def test_missing_zset_returns_empty(self):
        r = MiniRedis()
        self.assertEqual(r.zrange("nope", 0, -1), [])
        self.assertEqual(r.zrange_by_score("nope", 0, 1), [])

    def test_aof_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / "mini.aof")
            r1 = MiniRedis(aof_path=path)
            r1.set("a", "1")
            r1.zadd("lb", 5.0, "x")
            r2 = MiniRedis(aof_path=path)     # 重放日志恢复
            self.assertEqual(r2.get("a"), "1")
            self.assertEqual(r2.zrange("lb", 0, -1), [("x", 5.0)])


if __name__ == "__main__":
    unittest.main()
