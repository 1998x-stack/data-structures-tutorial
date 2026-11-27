import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from interview_problems import (
    LRUCache,
    build_list,
    climb_stairs,
    detect_cycle,
    inorder_traversal,
    inorder_traversal_iterative,
    is_valid,
    length_of_lis,
    level_order,
    longest_common_subsequence,
    max_sliding_window,
    merge_k_lists,
    num_islands,
    three_sum,
    to_list,
    trap,
    two_sum,
)


class TestHashing(unittest.TestCase):
    def test_two_sum_found_and_missing(self):
        self.assertEqual(two_sum([2, 7, 11, 15], 9), [0, 1])
        self.assertEqual(two_sum([1, 2, 3], 100), [-1, -1])

    def test_two_sum_duplicates_and_negatives(self):
        self.assertEqual(two_sum([3, 3], 6), [0, 1])
        self.assertEqual(two_sum([-3, 4, 3, 90], 0), [0, 2])

    def test_three_sum(self):
        self.assertEqual(three_sum([-1, 0, 1, 2, -1, -4]), [[-1, -1, 2], [-1, 0, 1]])

    def test_three_sum_all_zeros_and_empty(self):
        self.assertEqual(three_sum([0, 0, 0, 0]), [[0, 0, 0]])
        self.assertEqual(three_sum([1, 2]), [])


class TestLinkedLists(unittest.TestCase):
    def test_detect_cycle_none(self):
        self.assertIsNone(detect_cycle(build_list([1, 2, 3])))

    def test_detect_cycle_entry(self):
        head = build_list([3, 2, 0, -4], pos=1)
        self.assertEqual(detect_cycle(head).val, 2)

    def test_merge_k_lists(self):
        lists = [build_list([1, 4, 5]), build_list([1, 3, 4]), build_list([2, 6])]
        self.assertEqual(to_list(merge_k_lists(lists)), [1, 1, 2, 3, 4, 4, 5, 6])

    def test_merge_k_lists_empty(self):
        self.assertEqual(to_list(merge_k_lists([None, None])), [])


class TestStacksQueues(unittest.TestCase):
    def test_valid_brackets(self):
        self.assertTrue(is_valid("()[]{}"))
        self.assertFalse(is_valid("(]"))
        self.assertFalse(is_valid("("))
        self.assertTrue(is_valid(""))

    def test_sliding_window(self):
        self.assertEqual(max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3),
                         [3, 3, 5, 5, 6, 7])

    def test_sliding_window_edges(self):
        self.assertEqual(max_sliding_window([], 3), [])
        self.assertEqual(max_sliding_window([4], 3), [])


class TestTrees(unittest.TestCase):
    def _tree(self):
        from interview_problems import TreeNode
        root = TreeNode(1, None, TreeNode(2, TreeNode(3)))
        return root

    def test_inorder_both(self):
        root = self._tree()
        self.assertEqual(inorder_traversal(root), [1, 3, 2])
        self.assertEqual(inorder_traversal_iterative(root), [1, 3, 2])

    def test_level_order(self):
        self.assertEqual(level_order(self._tree()), [[1], [2], [3]])
        self.assertEqual(level_order(None), [])

    def test_num_islands(self):
        grid = [["1", "1", "0"], ["0", "1", "0"], ["0", "0", "1"]]
        self.assertEqual(num_islands(grid), 2)
        self.assertEqual(num_islands([]), 0)


class TestDP(unittest.TestCase):
    def test_climb_stairs(self):
        self.assertEqual([climb_stairs(n) for n in (1, 2, 3, 5)], [1, 2, 3, 8])

    def test_lis(self):
        self.assertEqual(length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]), 4)
        self.assertEqual(length_of_lis([]), 0)
        self.assertEqual(length_of_lis([7, 7, 7]), 1)

    def test_lcs(self):
        self.assertEqual(longest_common_subsequence("abcde", "ace"), 3)
        self.assertEqual(longest_common_subsequence("abc", "def"), 0)

    def test_trap(self):
        self.assertEqual(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]), 6)
        self.assertEqual(trap([]), 0)


class TestLRU(unittest.TestCase):
    def test_eviction_order(self):
        c = LRUCache(2)
        c.put(1, 1)
        c.put(2, 2)
        self.assertEqual(c.get(1), 1)
        c.put(3, 3)
        self.assertEqual(c.get(2), -1)
        self.assertEqual(c.get(3), 3)

    def test_update_existing(self):
        c = LRUCache(2)
        c.put(1, 1)
        c.put(1, 10)
        self.assertEqual(c.get(1), 10)

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            LRUCache(0)


if __name__ == "__main__":
    unittest.main()
