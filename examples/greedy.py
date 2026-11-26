"""Reference greedy routines for chapter 18. Pure standard library.

Run: python -m unittest discover -s tests
"""
import heapq


def coin_greedy(coins, amount):
    """Greedy fewest coins. Correct only for canonical systems (e.g. 1,2,5).

    Provided to contrast with DP coin_change; it is NOT correct for all inputs.
    """
    coins = sorted(coins, reverse=True)
    count = 0
    for coin in coins:
        if coin <= amount:
            take, amount = divmod(amount, coin)
            count += take
    return count if amount == 0 else -1


def activity_selection(activities):
    """Max set of non-overlapping half-open intervals, earliest finish first."""
    count, last_end = 0, float("-inf")
    for start, end in sorted(activities, key=lambda a: a[1]):
        if start >= last_end:
            count += 1
            last_end = end
    return count


def erase_overlap_intervals(intervals):
    """Fewest intervals to remove so the rest do not overlap."""
    if not intervals:
        return 0
    kept = activity_selection(intervals)
    return len(intervals) - kept


def huffman_wpl(freqs):
    """Weighted path length of a Huffman tree, built by merging the two lightest."""
    heap = list(freqs)
    heapq.heapify(heap)
    wpl = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        wpl += a + b
        heapq.heappush(heap, a + b)
    return wpl


def can_jump_greedy(nums):
    """Whether the last index is reachable; O(n), O(1) space."""
    reach = 0
    for i, step in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + step)
    return True


def can_jump_dp(nums):
    """Reference O(n^2) DP used to cross-check the greedy version on small inputs."""
    n = len(nums)
    dp = [False] * n
    dp[0] = True
    for i in range(1, n):
        for j in range(i):
            if dp[j] and j + nums[j] >= i:
                dp[i] = True
                break
    return dp[-1] if n else False
