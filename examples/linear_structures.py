"""Runnable reference implementations for chapters 04–08.

Python 3.12+, standard library only. Complexity assumes constant-cost key operations
and a random-access machine model, unless otherwise noted.
"""
from __future__ import annotations

from collections import OrderedDict, defaultdict, deque
from dataclasses import dataclass
from typing import Optional


@dataclass(eq=False)
class Node:
    value: int
    next: Optional["Node"] = None


def from_values(values):
    head = None
    for item in reversed(list(values)):
        head = Node(item, head)
    return head


def linked_values(head, limit=10_000):
    """Reject cycles while converting a finite linked list to Python values."""
    out, seen = [], set()
    while head is not None:
        if id(head) in seen:
            raise ValueError("cycle detected")
        seen.add(id(head))
        out.append(head.value)
        if len(out) > limit:
            raise ValueError("limit exceeded")
        head = head.next
    return out


def remove_value(head, target):
    dummy = Node(0, head)
    prev = dummy
    while prev.next is not None:
        if prev.next.value == target:
            prev.next = prev.next.next
        else:
            prev = prev.next
    return dummy.next


def reverse_list(head):
    prev = None
    cur = head
    while cur is not None:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    return prev


def has_cycle(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


class Stack:
    def __init__(self):
        self._data = []

    def push(self, value):
        self._data.append(value)

    def pop(self):
        if not self._data:
            raise IndexError("empty stack")
        return self._data.pop()

    def peek(self):
        if not self._data:
            raise IndexError("empty stack")
        return self._data[-1]


def valid_brackets(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    openers = set(pairs.values())
    stack = []
    for ch in text:
        if ch in openers:
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            raise ValueError("only bracket tokens are allowed")
    return not stack


def evaluate_rpn(tokens):
    stack = []
    for token in tokens:
        if token in {"+", "-", "*"}:
            if len(stack) < 2:
                raise ValueError("missing operand")
            b, a = stack.pop(), stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            else:
                stack.append(a * b)
        else:
            stack.append(int(token))
    if len(stack) != 1:
        raise ValueError("invalid expression")
    return stack[0]


def daily_temperatures(t):
    wait = [0] * len(t)
    stack = []
    for i, value in enumerate(t):
        while stack and t[stack[-1]] < value:
            j = stack.pop()
            wait[j] = i - j
        stack.append(i)
    return wait


def largest_rectangle_area(heights):
    if any(h < 0 for h in heights):
        raise ValueError("heights must be nonnegative")
    stack, best = [-1], 0
    for i, height in enumerate([*heights, 0]):
        while stack[-1] != -1 and heights[stack[-1]] > height:
            h = heights[stack.pop()]
            best = max(best, h * (i - stack[-1] - 1))
        stack.append(i)
    return best


class CircularQueue:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._a = [None] * capacity
        self._front = self._rear = self._size = 0

    def enqueue(self, value):
        if self._size == len(self._a):
            raise OverflowError("queue is full")
        self._a[self._rear] = value
        self._rear = (self._rear + 1) % len(self._a)
        self._size += 1

    def dequeue(self):
        if self._size == 0:
            raise IndexError("queue is empty")
        value = self._a[self._front]
        self._a[self._front] = None
        self._front = (self._front + 1) % len(self._a)
        self._size -= 1
        return value

    def __len__(self):
        return self._size


def sliding_window_max(nums, k):
    if not 1 <= k <= len(nums):
        raise ValueError("require 1 <= k <= len(nums)")
    candidates = deque()
    result = []
    for i, value in enumerate(nums):
        while candidates and candidates[0] <= i - k:
            candidates.popleft()
        while candidates and nums[candidates[-1]] <= value:
            candidates.pop()
        candidates.append(i)
        if i >= k - 1:
            result.append(nums[candidates[0]])
    return result


def bfs_distance(adj, start):
    dist, q = {start: 0}, deque([start])
    while q:
        u = q.popleft()
        for v in adj.get(u, ()):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def toy_bucket(key, bucket_count=5):
    if bucket_count <= 0:
        raise ValueError("bucket count must be positive")
    return key % bucket_count


def two_sum_unsorted(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        comp = target - x
        if comp in seen:
            return seen[comp], i
        seen[x] = i
    return None


class LRUCache:
    """Educational API: None means miss and therefore cannot be stored."""
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.entries = OrderedDict()

    def get(self, key):
        if key not in self.entries:
            return None
        self.entries.move_to_end(key)
        return self.entries[key]

    def put(self, key, value):
        if value is None:
            raise ValueError("None is reserved for misses")
        self.entries[key] = value
        self.entries.move_to_end(key)
        if len(self.entries) > self.capacity:
            self.entries.popitem(last=False)


@dataclass(eq=False)
class TreeNode:
    value: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def sample_tree():
    return TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)),
                    TreeNode(6, TreeNode(5)))


def preorder(root):
    out = []
    def walk(node):
        if node is None:
            return
        out.append(node.value)
        walk(node.left)
        walk(node.right)
    walk(root)
    return out


def inorder(root):
    out = []
    def walk(node):
        if node is None:
            return
        walk(node.left)
        out.append(node.value)
        walk(node.right)
    walk(root)
    return out


def postorder(root):
    out = []
    def walk(node):
        if node is None:
            return
        walk(node.left)
        walk(node.right)
        out.append(node.value)
    walk(root)
    return out


def preorder_iter(root):
    if root is None:
        return []
    out, stack = [], [root]
    while stack:
        node = stack.pop()
        out.append(node.value)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return out


def level_order(root):
    if root is None:
        return []
    result, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.value)
            for child in (node.left, node.right):
                if child is not None:
                    q.append(child)
        result.append(level)
    return result


def height_edges(node):
    if node is None:
        return -1
    return 1 + max(height_edges(node.left), height_edges(node.right))
