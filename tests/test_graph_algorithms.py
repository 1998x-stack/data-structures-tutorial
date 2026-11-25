"""Deterministic tests for chapter 13 graph algorithms."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from graph_algorithms import (
    dijkstra,
    bellman_ford,
    topological_sort,
    kruskal_mst,
    UnionFind,
)

FIG = {"A": [("B", 4), ("C", 2)], "B": [("C", 1), ("D", 5)], "C": [("D", 8)], "D": []}


class DijkstraTests(unittest.TestCase):
    def test_distances_match_figure(self):
        self.assertEqual(dijkstra(FIG, "A"), {"A": 0, "B": 4, "C": 2, "D": 9})

    def test_unreachable_vertex_is_absent(self):
        self.assertEqual(dijkstra({"A": [], "Z": []}, "A"), {"A": 0})

    def test_positive_weights_ignore_equal_paths(self):
        graph = {"A": [("B", 1), ("C", 1)], "B": [("D", 1)], "C": [("D", 1)], "D": []}
        self.assertEqual(dijkstra(graph, "A")["D"], 2)


class BellmanFordTests(unittest.TestCase):
    def test_negative_edge_is_allowed(self):
        self.assertEqual(bellman_ford(3, [(0, 1, 1), (1, 2, -2)], 0), [0, 1, -1])

    def test_negative_cycle_reports_none(self):
        self.assertIsNone(bellman_ford(3, [(0, 1, 1), (1, 2, -2), (2, 1, -2)], 0))


class TopoSortTests(unittest.TestCase):
    def test_acyclic_order_and_empty(self):
        order = topological_sort({0: [1, 2], 1: [3], 2: [3], 3: []}, [0, 1, 2, 3])
        self.assertIsNotNone(order)
        self.assertTrue(order.index(0) < order.index(3))
        self.assertEqual(topological_sort({}, []), [])

    def test_cycle_returns_none(self):
        self.assertIsNone(topological_sort({0: [1], 1: [2], 2: [0]}, [0, 1, 2]))


class MstTests(unittest.TestCase):
    EDGES = [(0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5), (2, 3, 8), (3, 4, 3)]

    def test_total_weight_and_edge_count(self):
        total, chosen = kruskal_mst(5, self.EDGES)
        self.assertEqual(total, 11)
        self.assertEqual(len(chosen), 4)  # n - 1 edges span all vertices

    def test_kruskal_avoids_cycle(self):
        _, chosen = kruskal_mst(3, [(0, 1, 1), (1, 2, 1), (0, 2, 1)])
        self.assertEqual(len(chosen), 2)

    def test_single_vertex_and_empty(self):
        self.assertEqual(kruskal_mst(1, []), (0, []))


class UnionFindTests(unittest.TestCase):
    def test_union_detects_cycle(self):
        uf = UnionFind(3)
        self.assertTrue(uf.union(0, 1))
        self.assertFalse(uf.union(1, 0))
        self.assertTrue(uf.union(1, 2))
        self.assertEqual(uf.find(0), uf.find(2))
