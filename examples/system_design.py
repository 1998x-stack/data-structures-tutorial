"""Reference snippets for chapter 25 system-design cases. Pure stdlib."""
import heapq
from collections import deque

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
_BASE = len(ALPHABET)


def base62_encode(num):
    if num < 0:
        raise ValueError("num must be non-negative")
    if num == 0:
        return ALPHABET[0]
    out = []
    while num > 0:
        num, rem = divmod(num, _BASE)
        out.append(ALPHABET[rem])
    return "".join(reversed(out))


def base62_decode(code):
    if not code:
        raise ValueError("empty code")
    num = 0
    for ch in code:
        if ch not in ALPHABET:
            raise ValueError("invalid character: " + ch)
        num = num * _BASE + ALPHABET.index(ch)
    return num


def top_k(scores, k):
    """Return the k highest (score, user) pairs, score descending."""
    if k <= 0:
        return []
    heap = []                              # min-heap of size <= k
    for user, score in scores.items():
        if len(heap) < k:
            heapq.heappush(heap, (score, user))
        elif score > heap[0][0]:
            heapq.heapreplace(heap, (score, user))
    return sorted(heap, key=lambda item: -item[0])


class SlidingWindowLimiter:
    def __init__(self, limit, window):
        if limit <= 0 or window <= 0:
            raise ValueError("limit and window must be positive")
        self.limit = limit
        self.window = window
        self.times = deque()               # request timestamps

    def allow(self, now):
        while self.times and self.times[0] <= now - self.window:
            self.times.popleft()           # drop requests outside the window
        if len(self.times) >= self.limit:
            return False
        self.times.append(now)
        return True


class TokenBucket:
    def __init__(self, rate, capacity):
        if rate <= 0 or capacity <= 0:
            raise ValueError("rate and capacity must be positive")
        self.rate = rate
        self.capacity = capacity
        self.tokens = float(capacity)
        self.last = None

    def allow(self, now):
        if self.last is None:
            self.last = now
        elapsed = now - self.last
        if elapsed < 0:
            raise ValueError("time must not go backwards")
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
