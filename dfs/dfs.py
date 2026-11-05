"""Depth-first search (DFS) demo.

A graph is a mapping from each vertex to the list of its neighbours, e.g.::

    graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B"],
        "E": ["B", "F"],
        "F": ["C", "E"],
    }

DFS explores as far as possible along one branch before backtracking.
This module shows the two usual implementations:

* recursive (``dfs_preorder``), which mirrors the definition directly;
* iterative with an explicit stack (``dfs_preorder_iterative``), which
  avoids Python's recursion limit on deep graphs.

It also shows two common applications: finding a path between two
vertices and flood-filling a 2D grid (counting islands).

Run ``python3 dfs.py`` to see a short demo.
"""
from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence

Graph = Mapping[str, Sequence[str]]


def _check_start(graph: Graph, start: str) -> None:
    if start not in graph:
        raise ValueError(f"start vertex {start!r} is not in the graph")


def dfs_preorder(graph: Graph, start: str) -> list[str]:
    """Return the vertices reachable from ``start`` in DFS preorder.

    Neighbours are visited in the order given by the adjacency list.
    Vertices already seen (for example through a cycle) are skipped, so
    each reachable vertex appears exactly once.
    """
    _check_start(graph, start)
    visited: set[str] = set()
    order: list[str] = []

    def visit(vertex: str) -> None:
        visited.add(vertex)
        order.append(vertex)
        for neighbour in graph.get(vertex, ()):
            if neighbour not in visited:
                visit(neighbour)

    visit(start)
    return order


def dfs_preorder_iterative(graph: Graph, start: str) -> list[str]:
    """Same result as :func:`dfs_preorder`, using an explicit stack.

    Neighbours are pushed in reverse so that the first neighbour in the
    adjacency list is popped first, which keeps the order identical to
    the recursive version.
    """
    _check_start(graph, start)
    visited: set[str] = set()
    order: list[str] = []
    stack = [start]

    while stack:
        vertex = stack.pop()
        if vertex in visited:
            continue
        visited.add(vertex)
        order.append(vertex)
        for neighbour in reversed(graph.get(vertex, ())):
            if neighbour not in visited:
                stack.append(neighbour)

    return order


def dfs_path(graph: Graph, start: str, goal: str) -> list[str] | None:
    """Return one DFS path from ``start`` to ``goal``, or ``None``.

    The result includes both endpoints. The search backtracks out of dead
    ends instead of giving up after the first branch.
    """
    _check_start(graph, start)
    if start == goal:
        return [start]

    visited = {start}
    # Each entry keeps the vertex and an iterator over its neighbours, so
    # a dead end can be popped and the search resumed at its parent.
    stack: list[tuple[str, Iterator[str]]] = [
        (start, iter(graph.get(start, ())))
    ]
    path = [start]

    while stack:
        vertex, neighbours = stack[-1]
        for neighbour in neighbours:
            if neighbour == goal:
                return path + [neighbour]
            if neighbour not in visited:
                visited.add(neighbour)
                path.append(neighbour)
                stack.append((neighbour, iter(graph.get(neighbour, ()))))
                break
        else:
            stack.pop()
            path.pop()

    return None


def connected_components(graph: Graph) -> list[list[str]]:
    """Return the connected components of an undirected graph.

    Vertices are returned in graph order, and each component is in DFS
    preorder. A new search starts from every vertex not reached yet, so
    disconnected parts are included.
    """
    visited: set[str] = set()
    components: list[list[str]] = []

    for start in graph:
        if start in visited:
            continue
        component: list[str] = []
        stack = [start]
        while stack:
            vertex = stack.pop()
            if vertex in visited:
                continue
            visited.add(vertex)
            component.append(vertex)
            for neighbour in reversed(graph.get(vertex, ())):
                if neighbour not in visited:
                    stack.append(neighbour)
        components.append(component)

    return components


def count_islands(grid: Sequence[Sequence[str]]) -> int:
    """Count islands of land in a rectangular grid.

    ``grid`` holds ``"1"`` (land) and ``"0"`` (water); cells are connected
    horizontally and vertically, not diagonally. The input is not
    modified: DFS marks visited cells in a separate set.

    >>> count_islands([["1", "0"], ["0", "1"]])
    2
    """
    if not grid or not grid[0]:
        return 0

    cols = len(grid[0])
    if any(len(row) != cols for row in grid):
        raise ValueError("grid must be rectangular")
    rows = len(grid)

    visited: set[tuple[int, int]] = set()
    islands = 0

    def flood(row: int, col: int) -> None:
        stack = [(row, col)]
        visited.add((row, col))
        while stack:
            r, c = stack.pop()
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and grid[nr][nc] == "1"
                    and (nr, nc) not in visited
                ):
                    visited.add((nr, nc))
                    stack.append((nr, nc))

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "1" and (row, col) not in visited:
                islands += 1
                flood(row, col)

    return islands


SAMPLE_GRAPH: dict[str, list[str]] = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"],
}

SAMPLE_GRID = [
    ["1", "1", "0", "0", "0"],
    ["1", "1", "0", "0", "1"],
    ["0", "0", "1", "0", "1"],
    ["0", "0", "0", "1", "1"],
]


def main() -> None:
    """Print a short tour of the functions above."""
    print("Graph (undirected):")
    for vertex, neighbours in SAMPLE_GRAPH.items():
        print(f"  {vertex}: {' '.join(neighbours)}")

    recursive = dfs_preorder(SAMPLE_GRAPH, "A")
    iterative = dfs_preorder_iterative(SAMPLE_GRAPH, "A")
    print(f"\nDFS preorder (recursive): {' -> '.join(recursive)}")
    print(f"DFS preorder (iterative): {' -> '.join(iterative)}")
    print(f"Same order: {recursive == iterative}")

    path = dfs_path(SAMPLE_GRAPH, "A", "F")
    print(f"\nPath A -> F: {' -> '.join(path) if path else 'not found'}")
    print(f"Connected components: {connected_components(SAMPLE_GRAPH)}")

    print("\nGrid ('1' = land, '0' = water):")
    for row in SAMPLE_GRID:
        print("  " + " ".join(row))
    print(f"Number of islands: {count_islands(SAMPLE_GRID)}")


if __name__ == "__main__":
    main()
