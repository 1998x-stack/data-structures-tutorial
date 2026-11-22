"""Deterministic exhaustive and regression tests for chapter 11."""
import itertools
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from heaps import MinHeap, heap_sort, is_min_heap


class MinHeapTests(unittest.TestCase):
    def test_push_pop_sorted_exhaustive(self):
        for length in range(6):
            for values in itertools.product((-1, 0, 2), repeat=length):
                heap = MinHeap()
                for value in values:
                    heap.push(value)
                self.assertTrue(is_min_heap(list(heap)))
                popped = [heap.pop() for _ in values]
                self.assertEqual(popped, sorted(values))

    def test_heapify_matches_sorted(self):
        for length in range(7):
            for values in itertools.permutations(range(length)):
                heap = MinHeap(values)
                self.assertTrue(is_min_heap(list(heap)))
                self.assertEqual([heap.pop() for _ in range(length)], sorted(values))

    def test_peek_does_not_remove(self):
        heap = MinHeap([5, 3, 8, 1])
        self.assertEqual(heap.peek(), 1)
        self.assertEqual(len(heap), 4)

    def test_empty_and_single(self):
        heap = MinHeap()
        self.assertIsNone(heap.peek())
        with self.assertRaises(IndexError):
            heap.pop()
        heap.push(7)
        self.assertEqual(heap.pop(), 7)
        with self.assertRaises(IndexError):
            heap.pop()


class HeapSortTests(unittest.TestCase):
    def test_sort_exhaustive(self):
        for length in range(7):
            for values in itertools.permutations(range(length)):
                self.assertEqual(heap_sort(values), sorted(values))
            for values in itertools.product((-2, 0, 2), repeat=length):
                self.assertEqual(heap_sort(values), sorted(values))

    def test_does_not_mutate_input(self):
        data = [3, 1, 2]
        heap_sort(data)
        self.assertEqual(data, [3, 1, 2])


if __name__ == "__main__":
    unittest.main()
