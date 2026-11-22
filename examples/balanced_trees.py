"""Runnable reference AVL / red-black material for chapter 10.

Python 3.12+, standard library only. Balance factor is
``height(left) - height(right)`` with the empty tree at height -1, so a leaf has
balance factor 0. The AVL routines below recompute subtree heights instead of
caching them; that keeps the teaching code short but makes one insert O(n log n)
in the worst case — production implementations store the height on each node.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import log2
from typing import Optional


@dataclass
class AvlNode:
    value: int
    left: Optional["AvlNode"] = None
    right: Optional["AvlNode"] = None


def height(node):
    if node is None:
        return -1
    return 1 + max(height(node.left), height(node.right))


def balance_factor(node):
    return 0 if node is None else height(node.left) - height(node.right)


def rotate_right(z):
    """LL / LR fix: y (z's left child) becomes the new subtree root."""
    y = z.left
    z.left = y.right
    y.right = z
    return y


def rotate_left(z):
    """RR / RL fix: y (z's right child) becomes the new subtree root."""
    y = z.right
    z.right = y.left
    y.left = z
    return y


def insert(root, value):
    """BST insert followed by one-or-two rotations on the way back up."""
    if root is None:
        return AvlNode(value)
    if value < root.value:
        root.left = insert(root.left, value)
    elif value > root.value:
        root.right = insert(root.right, value)
    else:
        return root  # duplicate keys are ignored
    return rebalance(root)


def rebalance(root):
    """Restore |balance factor| <= 1 at ``root`` using its two children."""
    factor = balance_factor(root)
    if factor > 1:
        if balance_factor(root.left) < 0:      # LR: left child leans right
            root.left = rotate_left(root.left)
        return rotate_right(root)              # LL or the second half of LR
    if factor < -1:
        if balance_factor(root.right) > 0:     # RL: right child leans left
            root.right = rotate_right(root.right)
        return rotate_left(root)               # RR or the second half of RL
    return root


def inorder(root):
    out, stack, node = [], [], root
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.value)
        node = node.right
    return out


def is_avl(root):
    """True iff every node keeps a balance factor in {-1, 0, 1}."""
    if root is None:
        return True
    return (abs(balance_factor(root)) <= 1
            and is_avl(root.left) and is_avl(root.right))


def avl_height_bound(n):
    """Classic AVL bound: height < 1.44 * log2(n + 2)."""
    return 1.44 * log2(n + 2)


def build(values):
    root = None
    for value in values:
        root = insert(root, value)
    return root


RED, BLACK = 0, 1


@dataclass
class RbNode:
    value: int
    color: int = RED
    left: Optional["RbNode"] = None
    right: Optional["RbNode"] = None


def is_red_black(root):
    """Check the colour rules (root black, no red-red, equal black height)."""
    if root is None:
        return True
    if root.color != BLACK:
        return False

    def black_height(node):
        if node is None:
            return 1  # every NIL leaf counts as one black node
        if node.color == RED and any(
                child is not None and child.color == RED
                for child in (node.left, node.right)):
            return None
        left = black_height(node.left)
        right = black_height(node.right)
        if left is None or right is None or left != right:
            return None
        return left + (1 if node.color == BLACK else 0)

    return black_height(root) is not None


def sample_red_black():
    """The tree drawn in figure 3: black root 13, red 8 / 17, black leaves."""
    return RbNode(
        13, BLACK,
        RbNode(8, RED, RbNode(1, BLACK), RbNode(11, BLACK)),
        RbNode(17, RED, RbNode(15, BLACK), RbNode(25, BLACK)),
    )
