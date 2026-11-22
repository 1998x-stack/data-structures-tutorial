"""Runnable reference min-heap for chapter 11.

Python 3.12+, standard library only. Indices are 0-based, matching the figures:
``parent(i) = (i-1)//2``, ``left(i) = 2i+1``, ``right(i) = 2i+2``.
Comparisons assume keys are totally ordered.
"""
from __future__ import annotations


class MinHeap:
    """A binary min-heap stored in a Python list."""

    def __init__(self, values=()):
        self._data = list(values)
        for i in range(len(self._data) // 2 - 1, -1, -1):
            self._sink(i)

    def push(self, value):
        self._data.append(value)
        self._swim(len(self._data) - 1)

    def pop(self):
        if not self._data:
            raise IndexError("pop from empty heap")
        top = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sink(0)
        return top

    def peek(self):
        return self._data[0] if self._data else None

    def _swim(self, i):
        data = self._data
        while i > 0:
            parent = (i - 1) // 2
            if data[i] >= data[parent]:
                break
            data[i], data[parent] = data[parent], data[i]
            i = parent

    def _sink(self, i):
        data = self._data
        n = len(data)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            smallest = i
            if left < n and data[left] < data[smallest]:
                smallest = left
            if right < n and data[right] < data[smallest]:
                smallest = right
            if smallest == i:
                break
            data[i], data[smallest] = data[smallest], data[i]
            i = smallest

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)


def is_min_heap(values):
    """True iff every node is >= its parent (0-based layout)."""
    return all(values[i] >= values[(i - 1) // 2] for i in range(1, len(values)))


def heap_sort(values):
    """Ascending in-place sort that reuses one max-heap, 0-based indices."""
    data = list(values)
    n = len(data)

    def sink(i, size):
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            largest = i
            if left < size and data[left] > data[largest]:
                largest = left
            if right < size and data[right] > data[largest]:
                largest = right
            if largest == i:
                return
            data[i], data[largest] = data[largest], data[i]
            i = largest

    for i in range(n // 2 - 1, -1, -1):
        sink(i, n)
    for end in range(n - 1, 0, -1):
        data[0], data[end] = data[end], data[0]
        sink(0, end)
    return data
