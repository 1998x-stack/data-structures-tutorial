"""Exhaustive small-case checks for chapter 19 union-find references."""
import itertools
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from union_find import (
    UnionFind, count_provinces, find_redundant_connection, num_islands, num_islands_bfs,
)


class UnionFindTests(unittest.TestCase):
    def test_basic_union_and_find(self):
        uf = UnionFind(5)
        self.assertEqual(uf.count, 5)
        self.assertFalse(uf.connected(0, 1))
        self.assertTrue(uf.union(0, 1))
        self.assertFalse(uf.union(0, 1))      # already connected
        self.assertTrue(uf.connected(0, 1))
        self.assertEqual(uf.count, 4)
        uf.union(1, 2)
        uf.union(3, 4)
        self.assertEqual(uf.count, 2)

    def test_empty_and_single(self):
        self.assertEqual(UnionFind(0).count, 0)
        uf = UnionFind(1)
        self.assertEqual(uf.find(0), 0)
        with self.assertRaises(ValueError):
            UnionFind(-1)

    def test_path_stays_flat(self):
        uf = UnionFind(1000)
        for i in range(1, 1000):
            uf.union(0, i)
        # Every node should now point directly at one root, depth <= 1.
        root = uf.find(500)
        for i in range(1000):
            self.assertEqual(uf.parent[i], root if i != root else uf.parent[root])

    def test_count_provinces(self):
        self.assertEqual(count_provinces([[1, 1, 0], [1, 1, 0], [0, 0, 1]]), 2)
        self.assertEqual(count_provinces([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), 3)
        self.assertEqual(count_provinces([]), 0)

    def test_find_redundant_connection(self):
        self.assertEqual(find_redundant_connection([[1, 2], [1, 3], [2, 3]]), [2, 3])
        self.assertEqual(find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]), [1, 4])

    def test_num_islands_matches_bfs(self):
        for rows in range(1, 4):
            for cols in range(1, 4):
                for cells in itertools.product("01", repeat=rows * cols):
                    grid = [list(cells[r * cols:(r + 1) * cols]) for r in range(rows)]
                    self.assertEqual(num_islands(grid), num_islands_bfs(grid), grid)
        self.assertEqual(num_islands([]), 0)
        self.assertEqual(num_islands([["0"]]), 0)
        self.assertEqual(num_islands([["1"]]), 1)


if __name__ == "__main__":
    unittest.main()
