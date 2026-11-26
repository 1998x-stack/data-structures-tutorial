"""Cases for chapter 22 skip list reference."""
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from skip_list import SkipList


def make(values, seed=22, max_level=16):
    sl = SkipList(max_level=max_level, rng=random.Random(seed))
    for v in values:
        sl.insert(v)
    return sl


class SkipListTests(unittest.TestCase):
    def test_empty(self):
        sl = SkipList(rng=random.Random(0))
        self.assertFalse(sl.search(1))
        self.assertFalse(sl.delete(1))
        self.assertEqual(sl.to_list(), [])
        self.assertEqual(sl.range(0, 10), [])

    def test_single(self):
        sl = make([5])
        self.assertTrue(sl.search(5))
        self.assertFalse(sl.search(4))
        self.assertEqual(sl.to_list(), [5])

    def test_duplicates_are_kept_in_order(self):
        sl = make([3, 1, 3, 2, 3])
        self.assertEqual(sl.to_list(), [1, 2, 3, 3, 3])

    def test_negatives_and_insertion_order(self):
        data = [0, -5, 7, -5, 3, -100, 42]
        sl = make(data)
        self.assertEqual(sl.to_list(), sorted(data))

    def test_range_boundaries(self):
        sl = make([1, 3, 5, 7, 9])
        self.assertEqual(sl.range(3, 7), [3, 5, 7])
        self.assertEqual(sl.range(3, 4), [3])
        self.assertEqual(sl.range(0, 100), [1, 3, 5, 7, 9])
        self.assertEqual(sl.range(6, 5), [])

    def test_random_shuffle_matches_sorted(self):
        rng = random.Random(1)
        vals = [rng.randint(-50, 50) for _ in range(200)]
        sl = make(vals, seed=7)
        self.assertEqual(sl.to_list(), sorted(vals))
        for v in vals:
            self.assertTrue(sl.search(v))

    def test_delete(self):
        sl = make([2, 4, 6, 8])
        self.assertTrue(sl.delete(6))
        self.assertFalse(sl.search(6))
        self.assertEqual(sl.to_list(), [2, 4, 8])
        self.assertFalse(sl.delete(6))

    def test_max_level_zero_is_plain_list(self):
        sl = make([5, 1, 3], max_level=0)
        self.assertEqual(sl.to_list(), [1, 3, 5])
        self.assertTrue(sl.search(3))

    def test_invalid_max_level(self):
        with self.assertRaises(ValueError):
            SkipList(max_level=-1)


if __name__ == "__main__":
    unittest.main()
