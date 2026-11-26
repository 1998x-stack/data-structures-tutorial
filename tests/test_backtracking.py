"""Exhaustive small-case checks for chapter 16 backtracking references."""
import itertools
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from backtracking import (
    permute, subsets, combine, combination_sum, solve_n_queens, cross_check_subsets,
)


class BacktrackingTests(unittest.TestCase):
    def test_permute_matches_itertools(self):
        for n in range(6):
            nums = list(range(1, n + 1))
            expected = [list(p) for p in itertools.permutations(nums)]
            self.assertEqual(permute(nums), expected)

    def test_subsets_matches_oracle_and_handles_duplicates(self):
        for n in range(6):
            nums = list(range(n))
            self.assertEqual({tuple(x) for x in subsets(nums)},
                             {tuple(x) for x in cross_check_subsets(nums)})
        self.assertEqual(sum(1 for _ in subsets([2, 2])), 4)
        self.assertEqual({tuple(x) for x in subsets([2, 2])}, {(), (2,), (2, 2)})
        self.assertEqual(subsets([]), [[]])

    def test_combine_matches_itertools(self):
        for n in range(1, 7):
            for k in range(n + 1):
                expected = [list(c) for c in itertools.combinations(range(1, n + 1), k)]
                self.assertEqual(combine(n, k), expected)

    def test_combination_sum_reuse_and_boundary(self):
        self.assertEqual(sorted(combination_sum([2, 3, 6, 7], 7)), [[2, 2, 3], [7]])
        self.assertEqual(combination_sum([2], 1), [])
        self.assertEqual(combination_sum([], 0), [[]])
        self.assertEqual(combination_sum([5], 3), [])

    def test_n_queens_known_counts(self):
        counts = [1, 1, 0, 0, 2, 10, 4, 40, 92]
        for n, expected in enumerate(counts):
            self.assertEqual(len(solve_n_queens(n)), expected, f"n={n}")

    def test_n_queens_solutions_are_valid(self):
        n = 6
        for placement in solve_n_queens(n):
            cols = set(placement)
            self.assertEqual(len(cols), n)
            self.assertEqual(len({r - c for r, c in enumerate(placement)}), n)
            self.assertEqual(len({r + c for r, c in enumerate(placement)}), n)


if __name__ == "__main__":
    unittest.main()
