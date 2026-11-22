"""Unit and small exhaustive checks for the first three lessons."""
import itertools
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from algorithms import (
    binary_search_leftmost, reverse_in_place, prefix_sums, range_sum,
    count_subarrays_sum_k, two_sum_sorted, longest_unique_substring
)

class FoundationsTests(unittest.TestCase):
    def test_binary_search(self):
        self.assertEqual(binary_search_leftmost([], 1), -1)
        self.assertEqual(binary_search_leftmost([1, 2, 2, 2, 5], 2), 1)
        self.assertEqual(binary_search_leftmost([1, 2, 3], 6), -1)

    def test_reverse(self):
        for values in ([], [1], [1, 2, 3], [1, 1]):
            a=list(values)
            self.assertEqual(reverse_in_place(a), list(reversed(values)))

    def test_prefix_ranges(self):
        for n in range(5):
            for a in itertools.product((-2, 0, 3), repeat=n):
                p = prefix_sums(a)
                for left in range(n + 1):
                    for right in range(left, n + 1):
                        self.assertEqual(range_sum(p, left, right), sum(a[left:right]))
        for left, right in ((-1, 1), (1, 0), (0, 7)):
            with self.assertRaises(ValueError):
                range_sum(prefix_sums([1, 2]), left, right)

    def test_subarrays_with_negative_values(self):
        for n in range(5):
            for a in itertools.product((-1, 0, 2), repeat=n):
                for k in range(-3, 5):
                    expected = sum(sum(a[l:r]) == k for l in range(n) for r in range(l + 1, n + 1))
                    self.assertEqual(count_subarrays_sum_k(a, k), expected)

    def test_two_sum(self):
        for n in range(5):
            for a in itertools.combinations_with_replacement((-2, 0, 1, 3), n):
                for target in range(-4, 7):
                    pair = two_sum_sorted(a, target)
                    exists = any(a[i] + a[j] == target for i in range(n) for j in range(i + 1, n))
                    self.assertEqual(pair is not None, exists)
                    if pair:
                        i,j=pair
                        self.assertTrue(0 <= i < j < n)
                        self.assertEqual(a[i] + a[j], target)

    def test_unique_window(self):
        for n in range(5):
            for chars in itertools.product("abc", repeat=n):
                s="".join(chars)
                expected=max((r-l for l in range(n+1) for r in range(l,n+1)
                              if len(set(s[l:r]))==r-l),default=0)
                self.assertEqual(longest_unique_substring(s), expected)

if __name__=="__main__":
    unittest.main()
