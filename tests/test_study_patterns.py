import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from study_patterns import (
    REVIEW_INTERVALS_DAYS,
    build,
    reverse_list_iterative,
    reverse_list_recursive,
    review_days,
    to_list,
    two_sum,
)


class TestReverseList(unittest.TestCase):
    def test_iterative_empty(self):
        self.assertEqual(to_list(reverse_list_iterative(None)), [])

    def test_iterative_single(self):
        self.assertEqual(to_list(reverse_list_iterative(build([7]))), [7])

    def test_iterative_basic(self):
        self.assertEqual(to_list(reverse_list_iterative(build([1, 2, 3, 4]))), [4, 3, 2, 1])

    def test_duplicates_and_negatives(self):
        data = [-1, 2, 2, -1]
        self.assertEqual(to_list(reverse_list_iterative(build(data))), list(reversed(data)))

    def test_recursive_matches_iterative(self):
        for data in ([], [1], [1, 2], [3, 1, 4, 1, 5]):
            self.assertEqual(
                to_list(reverse_list_recursive(build(data))),
                to_list(reverse_list_iterative(build(data))),
            )


class TestTwoSum(unittest.TestCase):
    def test_found(self):
        self.assertEqual(two_sum([2, 7, 11, 15], 9), [0, 1])

    def test_duplicates(self):
        self.assertEqual(two_sum([3, 3], 6), [0, 1])

    def test_negatives(self):
        self.assertEqual(two_sum([-3, 4, 3, 90], 0), [0, 2])

    def test_no_solution(self):
        self.assertEqual(two_sum([1, 2, 3], 100), [-1, -1])

    def test_empty(self):
        self.assertEqual(two_sum([], 0), [-1, -1])


class TestReviewDays(unittest.TestCase):
    def test_default_intervals(self):
        self.assertEqual(review_days(0), REVIEW_INTERVALS_DAYS)

    def test_offset_start(self):
        self.assertEqual(review_days(10), [11, 13, 17, 40])

    def test_custom_and_empty_intervals(self):
        self.assertEqual(review_days(5, [2, 9]), [7, 14])
        self.assertEqual(review_days(5, []), [])


if __name__ == "__main__":
    unittest.main()
