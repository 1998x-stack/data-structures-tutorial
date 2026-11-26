"""Reference range-query structures for chapter 20. Pure standard library.

Run: python -m unittest discover -s tests
"""


class SegmentTree:
    """Segment tree for range sum with point updates (no lazy propagation)."""

    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * max(self.n, 1))
        if self.n:
            self._build(0, 0, self.n - 1, list(arr))

    def _build(self, node, lo, hi, arr):
        if lo == hi:                       # leaf stores one element
            self.tree[node] = arr[lo]
            return
        mid = (lo + hi) // 2
        self._build(2 * node + 1, lo, mid, arr)
        self._build(2 * node + 2, mid + 1, hi, arr)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def update(self, idx, val):
        if not 0 <= idx < self.n:
            raise IndexError("index out of range")
        self._update(0, 0, self.n - 1, idx, val)

    def _update(self, node, lo, hi, idx, val):
        if lo == hi:
            self.tree[node] = val
            return
        mid = (lo + hi) // 2
        if idx <= mid:
            self._update(2 * node + 1, lo, mid, idx, val)
        else:
            self._update(2 * node + 2, mid + 1, hi, idx, val)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def query(self, l, r):
        if self.n == 0:
            return 0
        if not 0 <= l <= r < self.n:
            raise IndexError("range out of bounds")
        return self._query(0, 0, self.n - 1, l, r)

    def _query(self, node, lo, hi, l, r):
        if r < lo or hi < l:               # disjoint: identity for sum
            return 0
        if l <= lo and hi <= r:            # fully covered
            return self.tree[node]
        mid = (lo + hi) // 2
        return (self._query(2 * node + 1, lo, mid, l, r)
                + self._query(2 * node + 2, mid + 1, hi, l, r))


class FenwickTree:
    """1-indexed Fenwick tree (binary indexed tree) over numbers."""

    def __init__(self, n):
        if n < 0:
            raise ValueError("size must be non-negative")
        self.n = n
        self.bit = [0] * (n + 1)

    @classmethod
    def from_array(cls, arr):
        tree = cls(len(arr))
        for i, value in enumerate(arr, start=1):
            tree.update(i, value)
        return tree

    def update(self, i, delta):
        if not 1 <= i <= self.n:
            raise IndexError("index must be 1-based and in range")
        while i <= self.n:
            self.bit[i] += delta
            i += i & (-i)                  # jump up to the next range

    def prefix(self, i):
        if not 0 <= i <= self.n:
            raise IndexError("prefix index out of range")
        total = 0
        while i > 0:
            total += self.bit[i]
            i -= i & (-i)                  # jump down
        return total

    def range_sum(self, l, r):
        if not 1 <= l <= r <= self.n:
            raise IndexError("range must be 1-based and in bounds")
        return self.prefix(r) - self.prefix(l - 1)
