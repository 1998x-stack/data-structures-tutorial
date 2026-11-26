"""Reference recursion / divide-and-conquer routines for chapter 15.

Run: python -m unittest discover -s tests
"""
import itertools
from functools import lru_cache


def factorial(n):
    """n! by single-branch recursion; base case n == 0."""
    if n < 0:
        raise ValueError("factorial defined for n >= 0")
    if n == 0:
        return 1
    return n * factorial(n - 1)


@lru_cache(maxsize=None)
def fib_memo(n):
    """F(n) with memoization: O(n) time instead of the naive O(2^n) tree."""
    if n < 0:
        raise ValueError("fib defined for n >= 0")
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


def hanoi_moves(n, source="A", target="C", auxiliary="B"):
    """Return the move list; length is 2**n - 1, the proven minimum."""
    if n <= 0:
        return []
    if n == 1:
        return [(source, target)]
    return (hanoi_moves(n - 1, source, auxiliary, target)
            + [(source, target)]
            + hanoi_moves(n - 1, auxiliary, target, source))


def first_at_least(a, target):
    """Leftmost index whose value >= target; equals len(a) if none. Half-open [lo, hi)."""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def binary_search(a, target):
    """Any index equal to target in a sorted sequence, else -1."""
    i = first_at_least(a, target)
    return i if i < len(a) and a[i] == target else -1


def hanoi_min_moves(n):
    """Closed form used by tests, kept separate from the move generator."""
    return (1 << n) - 1 if n > 0 else 0
