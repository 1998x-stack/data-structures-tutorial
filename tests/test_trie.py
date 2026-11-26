"""Cases for chapter 21 trie references."""
import sys
import unittest
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from trie import Trie, BinaryTrie, find_max_xor


class TrieTests(unittest.TestCase):
    def test_empty_and_single(self):
        t = Trie()
        self.assertFalse(t.search("a"))
        self.assertFalse(t.starts_with("a"))
        self.assertEqual(t.autocomplete("a"), [])
        t.insert("a")
        self.assertTrue(t.search("a"))
        self.assertTrue(t.starts_with("a"))

    def test_prefix_is_not_a_word(self):
        t = Trie()
        t.insert("apple")
        self.assertFalse(t.search("app"))       # "app" was never inserted
        self.assertTrue(t.starts_with("app"))
        self.assertTrue(t.search("apple"))

    def test_word_can_be_a_prefix_of_another(self):
        t = Trie()
        for word in ("apple", "app", "apply", "application", "apt"):
            t.insert(word)
        self.assertTrue(t.search("app"))
        self.assertEqual(t.autocomplete("app"),
                         ["app", "apple", "apply", "application"])
        self.assertEqual(t.autocomplete("ap"),
                         ["app", "apple", "apply", "application", "apt"])
        self.assertEqual(t.autocomplete("z"), [])

    def test_duplicate_inserts_are_idempotent(self):
        t = Trie()
        t.insert("go")
        t.insert("go")
        self.assertEqual(t.autocomplete("g"), ["go"])

    def test_remove_prunes_and_keeps_shared_prefixes(self):
        t = Trie()
        for word in ("app", "apple", "apply"):
            t.insert(word)
        self.assertTrue(t.remove("apply"))
        self.assertFalse(t.search("apply"))
        self.assertTrue(t.starts_with("appl"))    # "apple" still present
        self.assertTrue(t.search("app"))
        self.assertFalse(t.remove("appl"))        # not a complete word
        self.assertTrue(t.remove("app"))
        self.assertTrue(t.remove("apple"))
        self.assertFalse(t.starts_with("a"))      # tail pruned

    def test_remove_missing_word(self):
        t = Trie()
        t.insert("cat")
        self.assertFalse(t.remove("car"))


class BinaryTrieTests(unittest.TestCase):
    def test_documented_example(self):
        self.assertEqual(find_max_xor([3, 10, 5, 25, 2, 8]), 28)

    def test_pairs_and_duplicates(self):
        self.assertEqual(find_max_xor([0, 0]), 0)
        self.assertEqual(find_max_xor([7, 7]), 0)
        self.assertEqual(find_max_xor([0, 5]), 5)

    def test_brute_force_cross_check(self):
        nums = [0, 1, 2, 7, 13, 31, 100, 1024]
        brute = max(a ^ b for a, b in combinations(nums, 2))
        self.assertEqual(find_max_xor(nums), brute)

    def test_errors(self):
        with self.assertRaises(ValueError):
            find_max_xor([1])
        with self.assertRaises(ValueError):
            BinaryTrie().insert(-1)


if __name__ == "__main__":
    unittest.main()
