"""Breadth-first search (BFS) demo.

A graph is a mapping from each vertex to the list of its neighbours, e.g.::

    graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B"],
        "E": ["B", "F"],
        "F": ["C", "E"],
    }

BFS explores vertices in order of their distance from the start: first the
start itself, then everything one edge away, then two edges away, and so
on. Visiting in that order is what makes BFS the usual choice for shortest
paths in unweighted graphs.

This module shows:

* the traversal itself (``bfs_order`` and ``bfs_levels``);
* shortest paths and distances (``bfs_path`` and ``shortest_distances``);
* two applications: testing whether a graph is bipartite and finding the
  shortest route through a grid.

Run ``python3 bfs.py`` to see a short demo.
"""
from __future__ import annotations

from collections import deque
from collections.abc import Mapping, Sequence
from typing import TypeVar

Graph = Mapping[str, Sequence[str]]
Cell = tuple[int, int]
Node = TypeVar("Node")


def _check_start(graph: Graph, start: str) -> None:
    if start not in graph:
        raise ValueError(f"start vertex {start!r} is not in the graph")


def _reconstruct(parent: Mapping[Node, Node | None], goal: Node) -> list[Node]:
    """Walk the parent links back from ``goal`` and return the path."""
    node = goal
    path = [node]
    while (previous := parent[node]) is not None:
        node = previous
        path.append(node)
    path.reverse()
    return path


def bfs_order(graph: Graph, start: str) -> list[str]:
    """Return the vertices reachable from ``start`` in BFS order.

    Vertices are listed by non-decreasing distance from ``start``; within a
    level, neighbours keep adjacency-list order. A vertex is marked as soon
    as it is enqueued, so a vertex reachable along several paths is still
    enqueued only once and cycles terminate.
    """
    _check_start(graph, start)
    visited = {start}
    order: list[str] = []
    queue = deque([start])

    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for neighbour in graph.get(vertex, ()):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    return order


def bfs_levels(graph: Graph, start: str) -> list[list[str]]:
    """Group the reachable vertices by distance from ``start``.

    ``levels[0]`` is ``[start]``, ``levels[1]`` holds its neighbours, and so
    on. The index of a level is the number of edges on a shortest path from
    ``start`` to every vertex in it.
    """
    _check_start(graph, start)
    visited = {start}
    levels: list[list[str]] = []
    frontier = [start]

    while frontier:
        levels.append(frontier)
        next_frontier: list[str] = []
        for vertex in frontier:
            for neighbour in graph.get(vertex, ()):
                if neighbour not in visited:
                    visited.add(neighbour)
                    next_frontier.append(neighbour)
        frontier = next_frontier

    return levels


def shortest_distances(graph: Graph, start: str) -> dict[str, int]:
    """Return the edge count of a shortest path to each reachable vertex.

    Unreachable vertices are omitted. Because BFS processes vertices in
    order of distance, the first time a vertex is reached is already via a
    shortest path.
    """
    _check_start(graph, start)
    distances = {start: 0}
    queue = deque([start])

    while queue:
        vertex = queue.popleft()
        for neighbour in graph.get(vertex, ()):
            if neighbour not in distances:
                distances[neighbour] = distances[vertex] + 1
                queue.append(neighbour)

    return distances


def bfs_path(graph: Graph, start: str, goal: str) -> list[str] | None:
    """Return a shortest path from ``start`` to ``goal``, or ``None``.

    Paths are measured in edges, so on an unweighted graph BFS finds one of
    the shortest possible answers (unlike DFS, which can return a long
    detour). The result includes both endpoints.
    """
    _check_start(graph, start)
    if start == goal:
        return [start]

    parent: dict[str, str | None] = {start: None}
    queue = deque([start])

    while queue:
        vertex = queue.popleft()
        for neighbour in graph.get(vertex, ()):
            if neighbour in parent:
                continue
            parent[neighbour] = vertex
            if neighbour == goal:
                return _reconstruct(parent, goal)
            queue.append(neighbour)

    return None


def is_bipartite(graph: Graph) -> bool:
    """Return whether the graph can be split into two independent groups.

    A graph is bipartite when its vertices can be coloured with two colours
    so that every edge joins different colours. BFS colours each vertex
    opposite to its parent; an edge to an already coloured vertex of the
    same colour proves the graph is not bipartite. Disconnected graphs are
    checked one component at a time.
    """
    colour: dict[str, int] = {}

    for start in graph:
        if start in colour:
            continue
        colour[start] = 0
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbour in graph.get(vertex, ()):
                if neighbour not in colour:
                    colour[neighbour] = 1 - colour[vertex]
                    queue.append(neighbour)
                elif colour[neighbour] == colour[vertex]:
                    return False

    return True


def shortest_path_grid(
    grid: Sequence[Sequence[str]], start: Cell, goal: Cell
) -> list[Cell] | None:
    """Return a shortest route between two open cells of a grid.

    ``grid`` holds ``"1"`` for walkable cells and ``"0"`` for walls; moves
    are horizontal or vertical, never diagonal. Both endpoints are included
    in the result, and ``None`` means ``goal`` is not reachable. The input
    is not modified.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if any(len(row) != cols for row in grid):
        raise ValueError("grid must be rectangular")

    for name, cell in (("start", start), ("goal", goal)):
        row, col = cell
        if not (0 <= row < rows and 0 <= col < cols):
            raise ValueError(f"{name} cell {cell!r} is outside the grid")
        if grid[row][col] != "1":
            raise ValueError(f"{name} cell {cell!r} is not walkable")

    parent: dict[Cell, Cell | None] = {start: None}
    queue = deque([start])

    while queue:
        current = queue.popleft()
        if current == goal:
            return _reconstruct(parent, goal)
        row, col = current
        for neighbour in (
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ):
            nrow, ncol = neighbour
            if (
                0 <= nrow < rows
                and 0 <= ncol < cols
                and grid[nrow][ncol] == "1"
                and neighbour not in parent
            ):
                parent[neighbour] = current
                queue.append(neighbour)

    return None


SAMPLE_GRAPH: dict[str, list[str]] = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"],
}

SAMPLE_GRID = [
    ["1", "1", "1", "0", "1"],
    ["0", "0", "1", "0", "1"],
    ["1", "1", "1", "1", "1"],
    ["1", "0", "0", "0", "1"],
    ["1", "1", "1", "1", "1"],
]


def main() -> None:
    """Print a short tour of the functions above."""
    print("Graph (undirected):")
    for vertex, neighbours in SAMPLE_GRAPH.items():
        print(f"  {vertex}: {' '.join(neighbours)}")

    print(f"\nBFS order from A: {' -> '.join(bfs_order(SAMPLE_GRAPH, 'A'))}")
    print(f"BFS levels: {bfs_levels(SAMPLE_GRAPH, 'A')}")
    print(f"Distances from A: {shortest_distances(SAMPLE_GRAPH, 'A')}")

    path = bfs_path(SAMPLE_GRAPH, "A", "F")
    if path is None:
        print("\nNo path A -> F")
    else:
        print(
            f"\nShortest path A -> F: {' -> '.join(path)} "
            f"({len(path) - 1} edges)"
        )
    print(f"Bipartite: {is_bipartite(SAMPLE_GRAPH)}")

    start, goal = (0, 0), (0, 4)
    route = shortest_path_grid(SAMPLE_GRID, start, goal)
    print("\nGrid ('1' = open, '0' = wall):")
    for row in SAMPLE_GRID:
        print("  " + " ".join(row))
    if route is None:
        print(f"No route {start} -> {goal}")
    else:
        print(
            f"Shortest route {start} -> {goal}: "
            f"{' -> '.join(str(cell) for cell in route)} "
            f"({len(route) - 1} moves)"
        )


if __name__ == "__main__":
    main()
