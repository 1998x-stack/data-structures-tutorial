"""Reference skip list for chapter 22. Pure standard library.

Run: python -m unittest discover -s tests
"""
import random


class SkipNode:
    __slots__ = ("value", "forward")

    def __init__(self, value, level):
        self.value = value
        self.forward = [None] * (level + 1)


class SkipList:
    def __init__(self, max_level=16, rng=None):
        if max_level < 0:
            raise ValueError("max_level must be non-negative")
        self.max_level = max_level
        self.rng = rng or random.Random()
        self.head = SkipNode(None, max_level)   # sentinel, holds no value
        self.level = 0

    def random_level(self):
        level = 0
        while self.rng.random() < 0.5 and level < self.max_level:
            level += 1
        return level

    def _find_update(self, value):
        update = [self.head] * (self.max_level + 1)
        node = self.head
        for i in range(self.level, -1, -1):
            while node.forward[i] and node.forward[i].value < value:
                node = node.forward[i]
            update[i] = node
        return update

    def insert(self, value):
        update = self._find_update(value)
        new_level = self.random_level()
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.head
            self.level = new_level
        node = SkipNode(value, new_level)
        for i in range(new_level + 1):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node

    def search(self, value):
        node = self.head
        for i in range(self.level, -1, -1):
            while node.forward[i] and node.forward[i].value < value:
                node = node.forward[i]
        node = node.forward[0]
        return node is not None and node.value == value

    def delete(self, value):
        update = self._find_update(value)
        target = update[0].forward[0]
        if target is None or target.value != value:
            return False
        for i in range(self.level + 1):
            if update[i].forward[i] is not target:
                break
            update[i].forward[i] = target.forward[i]
        while self.level > 0 and self.head.forward[self.level] is None:
            self.level -= 1
        return True

    def range(self, low, high):
        if low > high:
            return []
        node = self.head
        for i in range(self.level, -1, -1):
            while node.forward[i] and node.forward[i].value < low:
                node = node.forward[i]
        result, node = [], node.forward[0]
        while node is not None and node.value <= high:
            result.append(node.value)
            node = node.forward[0]
        return result

    def to_list(self):
        result, node = [], self.head.forward[0]
        while node is not None:
            result.append(node.value)
            node = node.forward[0]
        return result
