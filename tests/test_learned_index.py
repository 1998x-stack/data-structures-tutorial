"""Cases for chapter 27 learned-index toy."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from learned_index import LearnedIndex


class LearnedIndexTests(unittest.TestCase):
    def test_empty(self):
        idx = LearnedIndex([])
        self.assertEqual(idx.find(3), -1)
        self.assertEqual(idx.search_span(3), (0, -1))

    def test_single(self):
        idx = LearnedIndex([5])
        self.assertEqual(idx.find(5), 0)
        self.assertEqual(idx.find(4), -1)

    def test_all_present_keys_are_found(self):
        keys = list(range(1, 16, 2))          # 1,3,...,15
        idx = LearnedIndex(keys)
        for k in keys:
            pos = idx.find(k)
            self.assertNotEqual(pos, -1)
            self.assertEqual(idx.keys[pos], k)

    def test_missing_keys_return_minus_one(self):
        idx = LearnedIndex(list(range(1, 16, 2)))
        for k in (0, 2, 8, 16):
            self.assertEqual(idx.find(k), -1)

    def test_negatives(self):
        keys = [-10, -5, 0, 5, 10]
        idx = LearnedIndex(keys)
        for k in keys:
            self.assertNotEqual(idx.find(k), -1)
        self.assertEqual(idx.find(-7), -1)

    def test_duplicates_still_locatable(self):
        idx = LearnedIndex([1, 1, 1, 5, 5, 9])
        for k in (1, 5, 9):
            pos = idx.find(k)
            self.assertEqual(idx.keys[pos], k)

    def test_span_contains_the_answer(self):
        keys = [2, 4, 6, 8, 10, 12, 14, 16]
        idx = LearnedIndex(keys)
        for k in keys:
            lo, hi = idx.search_span(k)
            self.assertTrue(lo <= idx.find(k) <= hi)

    def test_predict_clamps_outside_range(self):
        idx = LearnedIndex([10, 20, 30, 40])
        self.assertEqual(idx.predict(-100), 0)
        self.assertEqual(idx.predict(100), len(idx.keys) - 1)


if __name__ == "__main__":
    unittest.main()
