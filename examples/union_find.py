"""Reference union-find for chapter 19. Pure standard library.

Run: python -m unittest discover -s tests
"""
from collections import deque


class UnionFind:
    """Disjoint-set union with path compression and union by rank."""

    def __init__(self, n):
        if n < 0:
            raise ValueError("size must be non-negative")
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n                 # number of disjoint sets

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:  # path compression, iterative
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False               # already connected
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.count -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)


def count_provinces(is_connected):
    """Number of connected components from an adjacency matrix."""
    n = len(is_connected)
    uf = UnionFind(n)
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                uf.union(i, j)
    return uf.count


def find_redundant_connection(edges):
    """Last edge that closes a cycle in an otherwise tree-like graph."""
    n = max(max(u, v) for u, v in edges)
    uf = UnionFind(n + 1)
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]
    return []


def num_islands(grid):
    """Count 4-connected islands of '1' using union-find."""
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    uf = UnionFind(rows * cols)
    ones = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1":
                continue
            ones += 1
            for dr, dc in ((1, 0), (0, 1)):
                nr, nc = r + dr, c + dc
                if nr < rows and nc < cols and grid[nr][nc] == "1":
                    uf.union(r * cols + c, nr * cols + nc)
    # isolate components fully made of water by ignoring them via a reparcount
    roots = {uf.find(r * cols + c) for r in range(rows) for c in range(cols)
             if grid[r][c] == "1"}
    return len(roots)


def num_islands_bfs(grid):
    """Independent BFS oracle so tests do not just compare a function to itself."""
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and not seen[r][c]:
                islands += 1
                queue = deque([(r, c)])
                seen[r][c] = True
                while queue:
                    cr, cc = queue.popleft()
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc] and grid[nr][nc] == "1":
                            seen[nr][nc] = True
                            queue.append((nr, nc))
    return islands
