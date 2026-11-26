"""Checks for chapter 18 greedy references, including a greedy counterexample."""
import itertools
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from greedy import (
    coin_greedy, activity_selection, erase_overlap_intervals,
    huffman_wpl, can_jump_greedy, can_jump_dp,
)
from dynamic_programming import coin_change


class GreedyTests(unittest.TestCase):
    def test_coin_greedy_counterexample(self):
        # Greedy is optimal for 1/2/5 but wrong for 1/3/4; DP is the safe choice.
        self.assertEqual(coin_greedy([1, 2, 5], 11), 3)
        self.assertEqual(coin_greedy([1, 3, 4], 6), 3)
        self.assertEqual(coin_change([1, 3, 4], 6), 2)
        self.assertLess(coin_change([1, 3, 4], 6), coin_greedy([1, 3, 4], 6))

    def test_activity_selection(self):
        acts = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 8), (5, 9),
                (6, 10), (8, 11), (8, 12), (2, 13), (12, 14)]
        self.assertEqual(activity_selection(acts), 4)
        self.assertEqual(activity_selection([]), 0)
        self.assertEqual(activity_selection([(5, 5)]), 1)

    def test_erase_overlap(self):
        self.assertEqual(erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]), 1)
        self.assertEqual(erase_overlap_intervals([]), 0)

    def test_huffman_wpl_matches_hand_calc(self):
        # Merge costs 14+25+30+55+100 = 224 for the 5,9,12,13,16,45 example.
        self.assertEqual(huffman_wpl([5, 9, 12, 13, 16, 45]), 224)
        self.assertEqual(huffman_wpl([1]), 0)
        self.assertEqual(huffman_wpl([1, 1]), 2)

    def test_can_jump_greedy_matches_dp(self):
        for n in range(1, 8):
            for nums in itertools.product((0, 1, 2, 3), repeat=n):
                self.assertEqual(can_jump_greedy(list(nums)), can_jump_dp(list(nums)), nums)
        self.assertTrue(can_jump_greedy([2, 3, 1, 1, 4]))
        self.assertFalse(can_jump_greedy([3, 2, 1, 0, 4]))
        self.assertTrue(can_jump_greedy([0]))


if __name__ == "__main__":
    unittest.main()
