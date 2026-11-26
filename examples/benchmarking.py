"""Runnable benchmarks and reference structures for chapter 26.

Pure standard library. Run the module to print timings for YOUR machine:
    python examples/benchmarking.py

Nothing here asserts absolute timings; the numbers depend on hardware and
on what else the machine is doing, so they are reported, never hard-coded.
"""
import timeit


class Node:
    __slots__ = ("value", "next")

    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self, values=()):
        self.head = None
        self.tail = None
        for value in values:
            self.append(value)

    def append(self, value):
        node = Node(value)
        if self.head is None:
            self.head = self.tail = node
            return
        self.tail.next = node
        self.tail = node

    def get(self, index):
        if index < 0:
            raise IndexError("negative index not supported")
        node = self.head
        for _ in range(index):
            if node is None:
                raise IndexError("index out of range")
            node = node.next
        if node is None:
            raise IndexError("index out of range")
        return node.value

    def traverse_sum(self):
        total, node = 0, self.head
        while node is not None:
            total += node.value
            node = node.next
        return total


def bench(n=10_000, repeat=200, seed=26):
    """Time list versus linked list on this machine. Returns a dict."""
    import random
    rng = random.Random(seed)
    arr = list(range(n))
    ll = LinkedList(range(n))
    idxs = [rng.randrange(n) for _ in range(100)]
    return {
        "n": n,
        "repeat": repeat,
        "traverse_array_s": timeit.timeit(lambda: sum(arr), number=repeat),
        "traverse_linked_s": timeit.timeit(ll.traverse_sum, number=repeat),
        "random_array_s": timeit.timeit(lambda: [arr[i] for i in idxs], number=repeat),
        "random_linked_s": timeit.timeit(lambda: [ll.get(i) for i in idxs], number=repeat),
    }


if __name__ == "__main__":
    for key, value in bench().items():
        print(f"{key}: {value}")
