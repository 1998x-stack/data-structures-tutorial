"""Exhaustive small-case checks for chapter 15 recursion references."""
import itertools
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from recursion import (
    factorial, fib_memo, hanoi_moves, hanoi_min_moves, first_at_least, binary_search,
)


class RecursionTests(unittest.TestCase):
    def test_factorial_matches_math(self):
        self.assertEqual(factorial(0), 1)
        for n in range(1, 11):
            self.assertEqual(factorial(n), math.factorial(n))
        with self.assertRaises(ValueError):
            factorial(-1)

    def test_fibonacci_base_and_growth(self):
        self.assertEqual([fib_memo(i) for i in range(8)], [0, 1, 1, 2, 3, 5, 8, 13])
        self.assertEqual(fib_memo(30), 832040)

    def test_hanoi_move_count_and_legality(self):
        for n in range(1, 7):
            moves = hanoi_moves(n)
            self.assertEqual(len(moves), hanoi_min_moves(n))
            self.assertEqual(len(moves), 2 ** n - 1 + (0 if n else 0))
            pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
            for src, dst in moves:
                disk = pegs[src].pop()
                if pegs[dst]:
                    self.assertLess(disk, pegs[dst][-1])
                pegs[dst].append(disk)
            self.assertEqual(pegs["C"], list(range(n, 0, -1)))

    def test_hanoi_empty(self):
        self.assertEqual(hanoi_moves(0), [])

    def test_boundary_search(self):
        for n in range(6):
            for a in itertools.combinations_with_replacement((-2, 0, 3), n):
                for target in range(-3, 5):
                    expected = next((i for i, x in enumerate(a) if x >= target), len(a))
                    self.assertEqual(first_at_least(a, target), expected)
                    hit = binary_search(a, target)
                    self.assertEqual(hit != -1, target in a)
                    if hit != -1:
                        self.assertEqual(a[hit], target)


if __name__ == "__main__":
    unittest.main()
