"""Deterministic exhaustive and regression tests for chapter 10."""
import itertools
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from balanced_trees import (
    BLACK, RED, AvlNode, RbNode, avl_height_bound, balance_factor, build,
    height, inorder, is_avl, is_red_black, rotate_left, rotate_right,
    sample_red_black,
)


class AvlInsertTests(unittest.TestCase):
    def test_inorder_and_balance_exhaustive(self):
        for length in range(7):
            for values in itertools.permutations(range(length)):
                root = build(values)
                self.assertEqual(inorder(root), list(range(length)))
                self.assertTrue(is_avl(root))
                self.assertLessEqual(height(root), avl_height_bound(length))

    def test_sorted_input_stays_logarithmic(self):
        n = 1000
        root = build(range(n))
        self.assertEqual(inorder(root), list(range(n)))
        self.assertTrue(is_avl(root))
        self.assertLessEqual(height(root), avl_height_bound(n))
        self.assertLess(height(root), 20)

    def test_duplicate_keys_ignored(self):
        root = build([2, 1, 2, 3, 3])
        self.assertEqual(inorder(root), [1, 2, 3])


class RotationTests(unittest.TestCase):
    def test_right_rotate_preserves_inorder(self):
        z = AvlNode(3, AvlNode(2, AvlNode(1)), AvlNode(4))
        self.assertEqual(inorder(z), [1, 2, 3, 4])
        y = rotate_right(z)
        self.assertEqual(y.value, 2)
        self.assertEqual(inorder(y), [1, 2, 3, 4])

    def test_left_rotate_preserves_inorder(self):
        z = AvlNode(2, AvlNode(1), AvlNode(3, None, AvlNode(4)))
        y = rotate_left(z)
        self.assertEqual(y.value, 3)
        self.assertEqual(inorder(y), [1, 2, 3, 4])

    def test_balance_factor_convention(self):
        self.assertEqual(height(None), -1)
        self.assertEqual(height(AvlNode(1)), 0)
        self.assertEqual(balance_factor(AvlNode(2, AvlNode(1))), 1)


class RedBlackTests(unittest.TestCase):
    def test_sample_tree_obeys_colour_rules(self):
        self.assertTrue(is_red_black(sample_red_black()))

    def test_root_must_be_black(self):
        tree = sample_red_black()
        tree.color = RED
        self.assertFalse(is_red_black(tree))

    def test_no_two_consecutive_red_nodes(self):
        tree = RbNode(3, BLACK, RbNode(2, RED, RbNode(1, RED)), RbNode(4, BLACK))
        self.assertFalse(is_red_black(tree))

    def test_black_heights_must_match(self):
        tree = RbNode(3, BLACK, RbNode(2, BLACK, RbNode(1, BLACK)), RbNode(4, BLACK))
        self.assertFalse(is_red_black(tree))

    def test_all_black_balanced_tree_is_valid(self):
        tree = RbNode(2, BLACK, RbNode(1, BLACK), RbNode(3, BLACK))
        self.assertTrue(is_red_black(tree))

    def test_single_black_node_is_valid(self):
        self.assertTrue(is_red_black(RbNode(1, BLACK)))
        self.assertFalse(is_red_black(RbNode(1, RED)))


if __name__ == "__main__":
    unittest.main()
