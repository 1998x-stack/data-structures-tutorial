"""Reference sorting algorithms for chapter 14. Pure standard library.

Run: python -m unittest discover -s tests
"""
import heapq
import random


def insertion_sort(a):
    """Stable, in place. O(n^2) worst/average, O(n) on nearly sorted input."""
    a = list(a)
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge(left, right):
    """Merge two sorted lists; <= keeps equal keys in left-before-right order."""
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out


def merge_sort(a):
    """Stable, O(n log n) always, O(n) extra space."""
    if len(a) <= 1:
        return list(a)
    mid = len(a) // 2
    return merge(merge_sort(a[:mid]), merge_sort(a[mid:]))


def _partition(a, lo, hi):
    pivot, i = a[hi], lo - 1
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1


def quick_sort(a):
    """Average O(n log n), worst O(n^2); not stable; random pivot avoids sorted-input blowup."""
    a = list(a)

    def rec(lo, hi):
        if lo >= hi:
            return
        r = random.randrange(lo, hi + 1)
        a[r], a[hi] = a[hi], a[r]
        p = _partition(a, lo, hi)
        rec(lo, p - 1); rec(p + 1, hi)

    rec(0, len(a) - 1)
    return a


def heap_sort(a):
    """Ascending order via heapq min-heap; O(n log n), O(n) extra here."""
    return list(heapq.nsmallest(len(a), a)) if a else []


def counting_sort(a):
    """Stable integer sort, O(n + k) where k = max - min + 1. Needs bounded range."""
    if not a:
        return []
    lo, hi = min(a), max(a)
    count = [0] * (hi - lo + 1)
    for x in a:
        count[x - lo] += 1
    out = []
    for value, times in enumerate(count):
        out.extend([value + lo] * times)
    return out


def radix_sort(a):
    """Stable LSD radix sort for non-negative ints, O(d * (n + 10))."""
    a = list(a)
    if any(x < 0 for x in a):
        raise ValueError("radix_sort expects non-negative integers")
    exp = 1
    while a and max(a) // exp > 0:
        buckets = [[] for _ in range(10)]
        for x in a:
            buckets[(x // exp) % 10].append(x)
        a = [x for bucket in buckets for x in bucket]
        exp *= 10
    return a
