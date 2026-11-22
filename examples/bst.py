"""Runnable reference BST for chapter 09.

Python 3.12+, standard library only. Policy: ``insert`` ignores duplicate keys;
comparisons assume keys are totally ordered and cheap to compare.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class BstNode:
    value: int
    left: Optional["BstNode"] = None
    right: Optional["BstNode"] = None


def build(values):
    root = None
    for value in values:
        root = insert(root, value)
    return root


def insert(root, value):
    """Insert one value, returning the (possibly new) root.

    Duplicated keys are ignored so that the in-order traversal stays strictly
    increasing, which ``validate`` relies on.
    """
    if root is None:
        return BstNode(value)
    if value < root.value:
        root.left = insert(root.left, value)
    elif value > root.value:
        root.right = insert(root.right, value)
    return root


def search(root, target):
    while root is not None and root.value != target:
        root = root.left if target < root.value else root.right
    return root


def delete(root, value):
    """Delete one occurrence, returning the (possibly new) root."""
    if root is None:
        return None
    if value < root.value:
        root.left = delete(root.left, value)
    elif value > root.value:
        root.right = delete(root.right, value)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        successor = root.right
        while successor.left is not None:
            successor = successor.left
        root.value = successor.value
        root.right = delete(root.right, successor.value)
    return root


def inorder(root):
    """Return keys in ascending order using an explicit stack."""
    out, stack, node = [], [], root
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.value)
        node = node.right
    return out


def validate(root):
    """True iff every node lies inside its subtree's open interval."""
    def check(node, low, high):
        if node is None:
            return True
        if low is not None and node.value <= low:
            return False
        if high is not None and node.value >= high:
            return False
        return (check(node.left, low, node.value)
                and check(node.right, node.value, high))
    return check(root, None, None)


def height_edges(node):
    """Height counted in edges: leaf = 0, empty = -1."""
    if node is None:
        return -1
    return 1 + max(height_edges(node.left), height_edges(node.right))


def sample_bst():
    """Fixed example: root 5, left 3(2,4), right 8(7,9)."""
    return build([5, 3, 8, 2, 4, 7, 9])
