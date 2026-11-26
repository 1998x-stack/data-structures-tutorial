"""Cross-checked cases for chapter 20 range-query references."""
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from range_queries import SegmentTree, FenwickTree


def brute_range(arr, l, r):
    return sum(arr[l:r + 1])


class SegmentTreeTests(unittest.TestCase):
    def test_empty_and_single(self):
        self.assertEqual(SegmentTree([]).query(0, 0), 0)
        st = SegmentTree([7])
        self.assertEqual(st.query(0, 0), 7)
        st.update(0, -3)
        self.assertEqual(st.query(0, 0), -3)

    def test_duplicates_negatives_and_boundaries(self):
        arr = [4, 4, -1, -1, 0, 9]
        st = SegmentTree(arr)
        for l in range(len(arr)):
            for r in range(l, len(arr)):
                self.assertEqual(st.query(l, r), brute_range(arr, l, r))

    def test_update_matches_rebuild(self):
        arr = [2, -5, 3, 3, 8]
        st = SegmentTree(arr)
        st.update(1, 10)
        arr[1] = 10
        for l in range(len(arr)):
            for r in range(l, len(arr)):
                self.assertEqual(st.query(l, r), brute_range(arr, l, r))

    def test_out_of_range_raises(self):
        st = SegmentTree([1, 2, 3])
        with self.assertRaises(IndexError):
            st.update(3, 0)
        with self.assertRaises(IndexError):
            st.query(2, 1)


class FenwickTreeTests(unittest.TestCase):
    def test_documented_example(self):
        ft = FenwickTree.from_array([1, 3, 5, 7, 9, 11])
        self.assertEqual(ft.range_sum(2, 5), 24)
        ft.update(3, 10)                 # arr[3] becomes 15
        self.assertEqual(ft.range_sum(2, 5), 34)

    def test_empty_and_single(self):
        self.assertEqual(FenwickTree(0).prefix(0), 0)
        one = FenwickTree.from_array([5])
        self.assertEqual(one.range_sum(1, 1), 5)

    def test_negatives_and_duplicates(self):
        arr = [3, -3, 3, 0, -1, -1]
        ft = FenwickTree.from_array(arr)
        for l in range(1, len(arr) + 1):
            for r in range(l, len(arr) + 1):
                self.assertEqual(ft.range_sum(l, r), brute_range(arr, l - 1, r - 1))

    def test_invalid_indices(self):
        ft = FenwickTree.from_array([1, 2])
        with self.assertRaises(IndexError):
            ft.update(0, 1)
        with self.assertRaises(IndexError):
            ft.range_sum(0, 1)
        with self.assertRaises(ValueError):
            FenwickTree(-1)


class CrossCheckTests(unittest.TestCase):
    def test_random_matches_brute_force(self):
        rng = random.Random(20)
        for _ in range(50):
            n = rng.randint(0, 12)
            arr = [rng.randint(-9, 9) for _ in range(n)]
            st = SegmentTree(arr)
            ft = FenwickTree.from_array(arr)
            for _ in range(8):
                if n and rng.random() < 0.5:
                    i = rng.randrange(n)
                    v = rng.randint(-9, 9)
                    st.update(i, v)
                    ft.update(i + 1, v - arr[i])
                    arr[i] = v
                if n:
                    l = rng.randrange(n)
                    r = rng.randrange(l, n)
                    self.assertEqual(st.query(l, r), brute_range(arr, l, r))
                    self.assertEqual(ft.range_sum(l + 1, r + 1), brute_range(arr, l, r))


if __name__ == "__main__":
    unittest.main()
