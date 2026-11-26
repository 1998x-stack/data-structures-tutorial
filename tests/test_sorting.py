"""Exhaustive small-case checks for chapter 14 sorting references."""
import itertools
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from sorting import (
    insertion_sort, merge_sort, quick_sort, heap_sort, counting_sort, radix_sort,
)

CASES = [(), (0,), (1, 1), (2, 1), (3, -1, 0, -1, 5), (5, 4, 3, 2, 1)]


class SortingTests(unittest.TestCase):
    def test_fixed_cases_each_algorithm(self):
        for a in CASES:
            expected = sorted(a)
            for fn in (insertion_sort, merge_sort, quick_sort, heap_sort):
                self.assertEqual(fn(a), expected, f"{fn.__name__} on {a}")

    def test_exhaustive_small_multisets(self):
        for n in range(6):
            for a in itertools.product((-2, 0, 1, 3), repeat=n):
                expected = sorted(a)
                self.assertEqual(merge_sort(a), expected)
                self.assertEqual(quick_sort(a), expected)
                self.assertEqual(insertion_sort(a), expected)

    def test_merge_is_stable_on_equal_keys(self):
        pairs = [(1, "a"), (1, "b"), (0, "c"), (1, "d")]
        merged = merge_sort(pairs)
        self.assertEqual(merged, [(0, "c"), (1, "a"), (1, "b"), (1, "d")])

    def test_linear_sorts_and_input_untouched(self):
        a = [170, 45, 75, -90, -802, 24, 2, 66, 2]
        self.assertEqual(counting_sort(a), sorted(a))
        self.assertEqual(insertion_sort(a), sorted(a))
        self.assertEqual(a[0], 170)  # input list not mutated

    def test_radix_rejects_negatives(self):
        self.assertEqual(radix_sort([0, 1000, 19, 19, 7]), [0, 7, 19, 19, 1000])
        with self.assertRaises(ValueError):
            radix_sort([1, -1])


if __name__ == "__main__":
    unittest.main()
