"""Cases for chapter 25 system-design reference snippets."""
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from system_design import (
    base62_encode, base62_decode, top_k, SlidingWindowLimiter, TokenBucket,
)


class Base62Tests(unittest.TestCase):
    def test_roundtrip(self):
        for n in (0, 1, 61, 62, 63, 12345, 2 ** 40):
            self.assertEqual(base62_decode(base62_encode(n)), n)

    def test_known_values(self):
        self.assertEqual(base62_encode(0), "0")
        self.assertEqual(base62_encode(61), "Z")

    def test_errors(self):
        with self.assertRaises(ValueError):
            base62_encode(-1)
        with self.assertRaises(ValueError):
            base62_decode("")
        with self.assertRaises(ValueError):
            base62_decode("a!")


class TopKTests(unittest.TestCase):
    def test_basic_and_k_larger_than_size(self):
        scores = {"alice": 950, "bob": 880, "carol": 990}
        self.assertEqual(top_k(scores, 2), [(990, "carol"), (950, "alice")])
        self.assertEqual(len(top_k(scores, 10)), 3)

    def test_k_zero_and_empty(self):
        self.assertEqual(top_k({"a": 1}, 0), [])
        self.assertEqual(top_k({}, 3), [])

    def test_duplicate_scores_and_negatives(self):
        scores = {"a": 5, "b": 5, "c": -3, "d": 0}
        result = top_k(scores, 2)
        self.assertEqual([s for s, _ in result], [5, 5])

    def test_matches_full_sort(self):
        rng = random.Random(25)
        scores = {f"u{i}": rng.randint(-100, 100) for i in range(200)}
        expected = sorted(((v, k) for k, v in scores.items()), key=lambda t: -t[0])[:5]
        self.assertEqual([s for s, _ in top_k(scores, 5)], [v for v, _ in expected])


class SlidingWindowTests(unittest.TestCase):
    def test_burst_over_limit_is_rejected(self):
        limiter = SlidingWindowLimiter(limit=3, window=1.0)
        results = [limiter.allow(t) for t in (0.0, 0.1, 0.2, 0.3)]
        self.assertEqual(results, [True, True, True, False])

    def test_window_slides_and_frees_capacity(self):
        limiter = SlidingWindowLimiter(limit=3, window=1.0)
        for t in (0.0, 0.1, 0.2):
            self.assertTrue(limiter.allow(t))
        self.assertFalse(limiter.allow(0.3))
        self.assertTrue(limiter.allow(1.5))   # all earlier stamps expired

    def test_invalid_args(self):
        with self.assertRaises(ValueError):
            SlidingWindowLimiter(0, 1.0)
        with self.assertRaises(ValueError):
            SlidingWindowLimiter(1, 0)


class TokenBucketTests(unittest.TestCase):
    def test_capacity_burst_then_refill(self):
        bucket = TokenBucket(rate=1.0, capacity=3)
        self.assertEqual([bucket.allow(0.0) for _ in range(4)],
                         [True, True, True, False])
        self.assertTrue(bucket.allow(5.0))     # refilled to capacity

    def test_time_must_not_go_backwards(self):
        bucket = TokenBucket(rate=1.0, capacity=2)
        bucket.allow(1.0)
        with self.assertRaises(ValueError):
            bucket.allow(0.5)


if __name__ == "__main__":
    unittest.main()
