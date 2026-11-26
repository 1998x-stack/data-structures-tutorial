"""Reference backtracking routines for chapter 16. Pure standard library.

Run: python -m unittest discover -s tests
"""
from itertools import combinations


def permute(nums):
    """All n! orderings of distinct values."""
    result = []
    used = [False] * len(nums)

    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])        # copy, not the live list
            return
        for i, value in enumerate(nums):
            if used[i]:
                continue
            path.append(value); used[i] = True
            backtrack(path)
            path.pop(); used[i] = False   # undo

    backtrack([])
    return result


def subsets(nums):
    """All 2**n subsets via start index, which prevents reordered duplicates."""
    result = []

    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result


def combine(n, k):
    """All k-element combinations of 1..n, with a remaining-count prune."""
    result = []

    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        for i in range(start, n + 1):
            if n - i + 1 < k - len(path):   # not enough numbers left
                break
            path.append(i)
            backtrack(i + 1, path)
            path.pop()

    backtrack(1, [])
    return result


def combination_sum(candidates, target):
    """All sums to target; each candidate may be reused; sorted input enables break."""
    candidates = sorted(candidates)
    result = []

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # i, not i+1: reuse
            path.pop()

    backtrack(0, [], target)
    return result


def solve_n_queens(n):
    """All placements of n non-attacking queens; diagonals keyed by row-col and row+col."""
    result = []

    def backtrack(row, cols, diag1, diag2, placement):
        if row == n:
            result.append(tuple(placement))
            return
        for col in range(n):
            d1, d2 = row - col, row + col
            if col in cols or d1 in diag1 or d2 in diag2:
                continue
            cols.add(col); diag1.add(d1); diag2.add(d2); placement.append(col)
            backtrack(row + 1, cols, diag1, diag2, placement)
            cols.discard(col); diag1.discard(d1); diag2.discard(d2); placement.pop()

    backtrack(0, set(), set(), set(), [])
    return result


def cross_check_subsets(nums):
    """Independent oracle so tests do not merely compare a function to itself."""
    out = []
    for r in range(len(nums) + 1):
        for pick in combinations(nums, r):
            out.append(list(pick))
    return out
