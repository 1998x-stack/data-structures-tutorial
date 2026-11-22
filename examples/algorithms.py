"""Data-structure foundations: small pure reference implementations.

No third-party packages required. Run: python -m unittest discover -s tests
"""
from collections import defaultdict

def binary_search_leftmost(a, target):
    """Find the first target in sorted sequence, or -1. O(log n) comparisons."""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo if lo < len(a) and a[lo] == target else -1

def reverse_in_place(a):
    left, right = 0, len(a) - 1
    while left < right:
        a[left], a[right] = a[right], a[left]
        left += 1
        right -= 1
    return a

def prefix_sums(a):
    p = [0]
    for x in a:
        p.append(p[-1] + x)
    return p

def range_sum(p, left, right):
    """Half-open range [left, right), where len(p)=len(array)+1."""
    if not 0 <= left <= right < len(p):
        raise ValueError("invalid half-open range")
    return p[right] - p[left]

def count_subarrays_sum_k(a, k):
    count = defaultdict(int)
    count[0] = 1
    prefix = answer = 0
    for x in a:
        prefix += x
        answer += count[prefix - k]
        count[prefix] += 1
    return answer

def two_sum_sorted(a, target):
    """Indices for any matching pair in ascending sorted sequence, else None."""
    left, right = 0, len(a) - 1
    while left < right:
        total = a[left] + a[right]
        if total == target:
            return (left, right)
        if total < target:
            left += 1
        else:
            right -= 1
    return None

def longest_unique_substring(s):
    """Length measured in Python Unicode code points."""
    seen = set()
    left = best = 0
    for right, char in enumerate(s):
        while char in seen:
            seen.remove(s[left])
            left += 1
        seen.add(char)
        best = max(best, right - left + 1)
    return best
