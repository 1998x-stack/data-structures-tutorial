"""Reference learned-index toy for chapter 27. Pure standard library.

A deliberately simple linear "model" plus local binary search. This is a
teaching sketch, not the full learned-index architecture.
"""


class LearnedIndex:
    def __init__(self, sorted_keys, window=4):
        self.keys = sorted(sorted_keys)
        self.window = window

    def predict(self, key):
        n = len(self.keys)
        if n <= 1:
            return 0
        lo, hi = self.keys[0], self.keys[-1]
        if hi == lo:
            return 0
        ratio = (key - lo) / (hi - lo)
        ratio = min(1.0, max(0.0, ratio))     # clamp outside the key range
        return int(ratio * (n - 1))

    def search_span(self, key):
        """The window [lo, hi] the model tells us to search (diagnostics)."""
        n = len(self.keys)
        if n == 0:
            return (0, -1)
        pos = self.predict(key)
        return (max(0, pos - self.window), min(n - 1, pos + self.window))

    def find(self, key):
        lo, hi = self.search_span(key)
        while lo <= hi:
            mid = (lo + hi) // 2
            if self.keys[mid] == key:
                return mid
            if self.keys[mid] < key:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1
