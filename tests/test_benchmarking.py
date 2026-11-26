"""Correctness checks for chapter 26 benchmarking helpers."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from benchmarking import LinkedList, bench


class LinkedListTests(unittest.TestCase):
    def test_empty(self):
        ll = LinkedList()
        self.assertEqual(ll.traverse_sum(), 0)
        with self.assertRaises(IndexError):
            ll.get(0)

    def test_single_and_duplicates(self):
        self.assertEqual(LinkedList([7]).traverse_sum(), 7)
        self.assertEqual(LinkedList([7]).get(0), 7)
        self.assertEqual(LinkedList([3, 3, 3]).traverse_sum(), 9)

    def test_negatives_match_builtin(self):
        data = [0, -1, 5, -100, 42]
        ll = LinkedList(data)
        self.assertEqual(ll.traverse_sum(), sum(data))
        self.assertEqual([ll.get(i) for i in range(len(data))], data)

    def test_get_out_of_range(self):
        ll = LinkedList([1, 2])
        with self.assertRaises(IndexError):
            ll.get(-1)
        with self.assertRaises(IndexError):
            ll.get(2)


class BenchTests(unittest.TestCase):
    def test_bench_returns_positive_timings(self):
        result = bench(n=500, repeat=5)
        self.assertEqual(result["n"], 500)
        for key in ("traverse_array_s", "traverse_linked_s",
                    "random_array_s", "random_linked_s"):
            self.assertGreater(result[key], 0.0)


if __name__ == "__main__":
    unittest.main()
