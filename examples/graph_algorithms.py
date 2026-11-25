"""Runnable reference graph algorithms for chapter 13.

Python 3.12+, standard library only. Weighted graphs are adjacency dicts
``{u: [(v, w), ...]}``; edge lists are ``[(u, v, w), ...]``. Weights may be
negative only for ``bellman_ford``. No third-party dependencies.
"""
from __future__ import annotations

import heapq


def dijkstra(graph, start):
    """Single-source shortest distances for non-negative weights.

    Returns a dict of settled distances. Requires every weight >= 0; with a
    negative edge the greedy "settle nearest first" order is no longer valid.
    """
    dist = {start: 0}
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, float("inf")):
            continue  # stale entry; u was already settled cheaper
        for v, w in graph[u]:
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist


def bellman_ford(n, edges, start):
    """Single-source distances with negative edges allowed.

    Returns a distance dict, or ``None`` if a negative cycle is reachable from
    ``start``. Vertices are integers ``0..n-1``.
    """
    dist = [float("inf")] * n
    dist[start] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    for u, v, w in edges:
        if dist[u] != float("inf") and dist[u] + w < dist[v]:
            return None
    return dist


def topological_sort(graph, vertices):
    """Kahn's topological order, or ``None`` if the digraph has a cycle."""
    from collections import deque

    indeg = {v: 0 for v in vertices}
    for u in graph:
        for v in graph[u]:
            indeg[v] += 1
    queue = deque(v for v in vertices if indeg[v] == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph.get(u, []):
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return order if len(order) == len(vertices) else None


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def kruskal_mst(n, edges):
    """Minimum spanning forest via Kruskal; returns (total_weight, chosen)."""
    uf = UnionFind(n)
    total, chosen = 0, []
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if uf.union(u, v):
            total += w
            chosen.append((u, v, w))
    return total, chosen
