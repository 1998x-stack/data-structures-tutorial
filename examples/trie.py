"""Reference trie structures for chapter 21. Pure standard library.

Run: python -m unittest discover -s tests
"""


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def _find_node(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search(self, word):
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        return self._find_node(prefix) is not None

    def autocomplete(self, prefix):
        node = self._find_node(prefix)
        if node is None:
            return []
        results = []
        self._collect(node, list(prefix), results)
        return results

    def _collect(self, node, path, results):
        if node.is_end:
            results.append("".join(path))
        for ch, child in node.children.items():
            path.append(ch)
            self._collect(child, path, results)   # enter and backtrack
            path.pop()

    def remove(self, word):
        node, stack = self.root, []
        for ch in word:
            if ch not in node.children:
                return False
            stack.append((node, ch))
            node = node.children[ch]
        if not node.is_end:
            return False
        node.is_end = False
        for parent, ch in reversed(stack):    # prune empty tail nodes
            child = parent.children[ch]
            if child.is_end or child.children:
                break
            del parent.children[ch]
        return True


class BinaryTrie:
    """Binary trie for maximum pairwise XOR over non-negative ints."""

    BITS = 31

    def __init__(self):
        self.root = [None, None]

    def insert(self, num):
        if num < 0:
            raise ValueError("only non-negative integers are supported")
        node = self.root
        for i in range(self.BITS, -1, -1):
            bit = (num >> i) & 1
            if node[bit] is None:
                node[bit] = [None, None]
            node = node[bit]

    def max_xor(self, num):
        node, best = self.root, 0
        for i in range(self.BITS, -1, -1):
            bit = (num >> i) & 1
            want = 1 - bit                 # prefer the opposite bit
            if node[want] is not None:
                best |= (1 << i)
                node = node[want]
            else:
                node = node[bit]
        return best


def find_max_xor(nums):
    if len(nums) < 2:
        raise ValueError("need at least two numbers")
    trie = BinaryTrie()
    trie.insert(nums[0])              # seed the trie
    best = 0
    for num in nums[1:]:
        best = max(best, trie.max_xor(num))
        trie.insert(num)
    return best
