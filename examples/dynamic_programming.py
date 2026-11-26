"""Reference dynamic-programming routines for chapter 17. Pure standard library.

Run: python -m unittest discover -s tests
"""
import bisect


def fib_dp(n):
    """Bottom-up Fibonacci in O(n) time, O(1) space (n >= 0)."""
    if n < 0:
        raise ValueError("fib defined for n >= 0")
    prev2, prev1 = 0, 1
    if n == 0:
        return 0
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev1 + prev2
    return prev1


def climb_stairs(n):
    """Ways to reach step n using 1- or 2-step moves."""
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def rob(nums):
    """Max sum of non-adjacent values."""
    prev2 = prev1 = 0
    for num in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + num)
    return prev1


def max_subarray(nums):
    """Kadane: largest sum of a non-empty contiguous subarray."""
    if not nums:
        raise ValueError("empty array has no subarray")
    cur = best = nums[0]
    for num in nums[1:]:
        cur = max(num, cur + num)
        best = max(best, cur)
    return best


def knap_01(weights, values, capacity):
    """0/1 knapsack: each item at most once. O(n*C)."""
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):   # descending: item used once
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


def coin_change(coins, amount):
    """Fewest coins to reach amount, unlimited supply; -1 if impossible."""
    INF = float("inf")
    dp = [0] + [INF] * amount
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1    # ascending: coins reusable
    return dp[amount] if dp[amount] != INF else -1


def unique_paths(m, n):
    """Paths from top-left to bottom-right moving right/down only."""
    row = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            row[j] += row[j - 1]
    return row[-1]


def min_distance(word1, word2):
    """Levenshtein edit distance with insert/delete/replace."""
    prev = list(range(len(word2) + 1))
    for i, ch1 in enumerate(word1, 1):
        cur = [i] + [0] * len(word2)
        for j, ch2 in enumerate(word2, 1):
            cost = 0 if ch1 == ch2 else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[-1]


def longest_common_subsequence(a, b):
    """Length of the longest common subsequence of two strings."""
    prev = [0] * (len(b) + 1)
    for ch1 in a:
        cur = [0]
        for j, ch2 in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if ch1 == ch2 else max(prev[j], cur[j - 1]))
        prev = cur
    return prev[-1]


def length_of_lis(nums):
    """Longest strictly increasing subsequence length in O(n log n)."""
    tails = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)


def longest_palindrome(s):
    """Longest palindromic substring by expanding around centers."""
    best = ""

    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]

    for i in range(len(s)):
        for candidate in (expand(i, i), expand(i, i + 1)):
            if len(candidate) > len(best):
                best = candidate
    return best
