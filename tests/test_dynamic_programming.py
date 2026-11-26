"""Exhaustive small-case checks for chapter 17 DP references."""
import itertools
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from dynamic_programming import (
    fib_dp, climb_stairs, rob, max_subarray, knap_01, coin_change,
    unique_paths, min_distance, longest_common_subsequence, length_of_lis, longest_palindrome,
)


class DpTests(unittest.TestCase):
    def test_fib_and_stairs(self):
        self.assertEqual([fib_dp(i) for i in range(9)], [0, 1, 1, 2, 3, 5, 8, 13, 21])
        self.assertEqual([climb_stairs(i) for i in range(6)], [1, 1, 2, 3, 5, 8])
        with self.assertRaises(ValueError):
            fib_dp(-1)

    def test_rob_matches_bruteforce(self):
        for n in range(7):
            for nums in itertools.product((0, 1, 2, 3), repeat=n):
                best = 0
                for mask in range(1 << n):
                    if any((mask >> k) & 3 == 3 for k in range(n - 1)):
                        continue
                    best = max(best, sum(nums[i] for i in range(n) if mask >> i & 1))
                self.assertEqual(rob(list(nums)), best)

    def test_max_subarray_including_negatives(self):
        self.assertEqual(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)
        self.assertEqual(max_subarray([-5]), -5)
        self.assertEqual(max_subarray([-3, -1, -7]), -1)
        with self.assertRaises(ValueError):
            max_subarray([])

    def test_knapsack_against_bruteforce(self):
        for n in range(5):
            for weights in itertools.product((1, 2, 3), repeat=n):
                values = [w * 2 + 1 for w in weights]
                for cap in range(7):
                    best = 0
                    for mask in range(1 << n):
                        if sum(weights[i] for i in range(n) if mask >> i & 1) <= cap:
                            best = max(best, sum(values[i] for i in range(n) if mask >> i & 1))
                    self.assertEqual(knap_01(list(weights), values, cap), best)

    def test_coin_change_and_unique_paths(self):
        self.assertEqual(coin_change([1, 2, 5], 11), 3)
        self.assertEqual(coin_change([2], 3), -1)
        self.assertEqual(coin_change([], 0), 0)
        self.assertEqual(unique_paths(3, 7), 28)
        self.assertEqual(unique_paths(1, 1), 1)

    def test_string_dp(self):
        self.assertEqual(min_distance("horse", "ros"), 3)
        self.assertEqual(min_distance("", "abc"), 3)
        self.assertEqual(min_distance("abc", "abc"), 0)
        self.assertEqual(longest_common_subsequence("abcde", "ace"), 3)
        self.assertEqual(longest_common_subsequence("", "abc"), 0)

    def test_lis_and_palindrome(self):
        self.assertEqual(length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]), 4)
        self.assertEqual(length_of_lis([3, 3, 3]), 1)
        self.assertEqual(length_of_lis([]), 0)
        self.assertEqual(longest_palindrome("babad"), "bab")
        self.assertEqual(longest_palindrome("cbbd"), "bb")
        self.assertEqual(longest_palindrome("a"), "a")


if __name__ == "__main__":
    unittest.main()
