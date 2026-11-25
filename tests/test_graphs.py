"""Deterministic tests for chapter 12 graph utilities."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from graphs import (
    build_adjacency,
    bfs_order,
    bfs_distances,
    bfs_shortest_path,
    dfs_order,
    connected_components,
    has_cycle_directed,
)


class BuildTests(unittest.TestCase):
    def test_undirected_lists_both_directions(self):
        graph = build_adjacency([(0, 1), (1, 2)])
        self.assertEqual(graph[0], [1])
        self.assertEqual(graph[1], [0, 2])
        self.assertEqual(graph[2], [1])

    def test_directed_lists_one_direction(self):
        graph = build_adjacency([(0, 1)], directed=True)
        self.assertEqual(graph[0], [1])
        self.assertEqual(graph[1], [])

    def test_empty_and_isolated_vertices(self):
        self.assertEqual(build_adjacency([]), {})
        graph = {"x": []}
        self.assertEqual(bfs_order(graph, "x"), ["x"])
        self.assertEqual(dfs_order(graph, "x"), ["x"])
        self.assertEqual(bfs_distances(graph, "x"), {"x": 0})


class TraversalTests(unittest.TestCase):
    def setUp(self):
        self.graph = build_adjacency([(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)])

    def test_orders_match_figure(self):
        self.assertEqual(bfs_order(self.graph, 0), [0, 1, 2, 3, 4])
        self.assertEqual(dfs_order(self.graph, 0), [0, 1, 3, 2, 4])

    def test_bfs_distance_is_layering(self):
        self.assertEqual(bfs_distances(self.graph, 0), {0: 0, 1: 1, 2: 1, 3: 2, 4: 3})

    def test_shortest_path_is_fewest_edges(self):
        self.assertEqual(bfs_shortest_path(self.graph, 0, 4), [0, 1, 3, 4])
        self.assertEqual(bfs_shortest_path(self.graph, 2, 2), [2])
        self.assertIsNone(bfs_shortest_path(build_adjacency([(0, 1)]), 0, 9))


class ComponentTests(unittest.TestCase):
    def test_two_components(self):
        graph = build_adjacency([(0, 1), (2, 3)])
        parts = {frozenset(c) for c in connected_components(graph)}
        self.assertEqual(parts, {frozenset({0, 1}), frozenset({2, 3})})

    def test_isolated_vertex_is_its_own_component(self):
        graph = {"a": ["b"], "b": ["a"], "c": []}
        self.assertEqual(len(connected_components(graph)), 2)


class CycleTests(unittest.TestCase):
    def test_dag_has_no_cycle(self):
        self.assertFalse(has_cycle_directed({0: [1, 2], 1: [2], 2: []}))

    def test_self_loop_and_back_edge(self):
        self.assertTrue(has_cycle_directed({0: [0]}))
        self.assertTrue(has_cycle_directed({0: [1], 1: [2], 2: [0]}))

    def test_shared_child_is_not_a_cycle(self):
        self.assertFalse(has_cycle_directed({0: [2], 1: [2], 2: []}))
