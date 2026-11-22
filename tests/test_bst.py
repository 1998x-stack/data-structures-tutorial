"""Deterministic exhaustive and regression tests for chapter 09 (BST)."""
import itertools
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from bst import (
    BstNode, build, delete, height_edges, inorder, insert, sample_bst, search,
    validate,
)


class BuildAndSearchTests(unittest.TestCase):
    def test_inorder_sorted_exhaustive_with_duplicates(self):
        for length in range(5):
            for values in itertools.product((-1, 0, 2), repeat=length):
                root = build(values)
                self.assertEqual(inorder(root), sorted(set(values)))
                self.assertTrue(validate(root))

    def test_search_hits_and_misses(self):
        root = sample_bst()
        for present in (2, 3, 4, 5, 7, 8, 9):
            hit = search(root, present)
            self.assertIsNotNone(hit)
            self.assertEqual(hit.value, present)
        for missing in (-3, 0, 1, 6, 10, 100):
            self.assertIsNone(search(root, missing))

    def test_duplicates_are_ignored_and_tree_unchanged(self):
        root = insert(sample_bst(), 5)
        self.assertEqual(inorder(root), [2, 3, 4, 5, 7, 8, 9])

    def test_negative_and_boundary_values(self):
        root = build([0, -5, 5, -10, 10])
        self.assertEqual(inorder(root), [-10, -5, 0, 5, 10])
        self.assertEqual(search(root, -10).value, -10)


class DeleteTests(unittest.TestCase):
    def test_delete_every_value_exhaustive(self):
        for values in itertools.permutations([3, 1, 5, 2, 4]):
            for target in (3, 1, 5, 2, 4, 99):
                root = build(values)
                result = delete(root, target)
                expected = sorted(v for v in set(values) if v != target)
                self.assertEqual(inorder(result), expected)
                self.assertTrue(validate(result))

    def test_delete_two_child_uses_inorder_successor(self):
        root = delete(build([5, 3, 8, 2, 4, 7, 9]), 3)
        self.assertEqual(inorder(root), [2, 4, 5, 7, 8, 9])
        self.assertTrue(validate(root))


class ValidateTests(unittest.TestCase):
    def test_rejects_violation_in_deeper_subtree(self):
        # root 5, left subtree 3 with a right child 6 -> 6 > 5 in left subtree.
        bad = BstNode(5, BstNode(3, None, BstNode(6)), BstNode(8))
        self.assertFalse(validate(bad))
        # The naive "left child < root < right child" check would accept it,
        # because only the direct children 3 and 8 are compared.
        self.assertTrue(bad.left.value < bad.value < bad.right.value)

    def test_accepts_arbitrary_valid_shapes(self):
        for values in itertools.permutations([4, 2, 6, 1, 3, 5, 7]):
            self.assertTrue(validate(build(values)))


class HeightAndBoundaryTests(unittest.TestCase):
    def test_empty_single_and_skew(self):
        self.assertEqual(inorder(None), [])
        self.assertIsNone(search(None, 1))
        self.assertIsNone(delete(None, 1))
        self.assertEqual(height_edges(None), -1)
        self.assertEqual(height_edges(BstNode(1)), 0)
        self.assertEqual(height_edges(build([1, 2, 3, 4, 5])), 4)

    def test_balanced_height_is_logarithmic(self):
        self.assertEqual(height_edges(build([3, 1, 5, 2, 4])), 2)
        self.assertEqual(height_edges(sample_bst()), 2)

    def test_delete_root_and_absent_value(self):
        root = build([2, 1, 3])
        self.assertEqual(inorder(delete(root, 2)), [1, 3])
        again = build([2, 1, 3])
        self.assertEqual(inorder(delete(again, 99)), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
