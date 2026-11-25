"""Runnable reference graph utilities for chapter 12.

Python 3.12+, standard library only. A graph is an adjacency dict
``{vertex: [neighbors]}``; vertex labels are hashable. Undirected graphs list
both directions, matching the figures. No third-party dependencies.
"""
from __future__ import annotations

from collections import deque


def build_adjacency(edges, directed=False):
    """Build an adjacency dict from an edge list."""
    graph = {}
    for u, v in edges:
        graph.setdefault(u, [])
        graph.setdefault(v, [])
        graph[u].append(v)
        if not directed:
            graph[v].append(u)
    return graph


def bfs_order(graph, start):
    """Breadth-first visit order from ``start`` (queue, first-seen wins)."""
    seen = {start}
    order = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return order


def bfs_distances(graph, start):
    """Fewest-edge distance from ``start`` to every reachable vertex."""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if nxt not in dist:
                dist[nxt] = dist[node] + 1
                queue.append(nxt)
    return dist


def bfs_shortest_path(graph, start, goal):
    """A fewest-edge path from ``start`` to ``goal``, or ``None``."""
    if start == goal:
        return [start]
    prev = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if nxt not in prev:
                prev[nxt] = node
                if nxt == goal:
                    path = [goal]
                    while path[-1] != start:
                        path.append(prev[path[-1]])
                    return path[::-1]
                queue.append(nxt)
    return None


def dfs_order(graph, start):
    """Depth-first preorder visit order (explicit stack)."""
    seen = set()
    order = []
    stack = [start]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        for nxt in reversed(graph[node]):
            if nxt not in seen:
                stack.append(nxt)
    return order


def connected_components(graph):
    """List the undirected connected components as vertex sets."""
    seen = set()
    components = []
    for start in graph:
        if start in seen:
            continue
        block = set()
        stack = [start]
        while stack:
            node = stack.pop()
            if node in block:
                continue
            block.add(node)
            seen.add(node)
            stack.extend(graph[node])
        components.append(block)
    return components


def has_cycle_directed(graph):
    """True if the directed graph has a cycle (three-colour DFS)."""
    WHITE, GRAY, BLACK = 0, 1, 2
    colour = {node: WHITE for node in graph}

    def visit(node):
        colour[node] = GRAY
        for nxt in graph.get(node, []):
            if colour[nxt] == GRAY:
                return True
            if colour[nxt] == WHITE and visit(nxt):
                return True
        colour[node] = BLACK
        return False

    return any(colour[n] == WHITE and visit(n) for n in graph)
