# Breadth-first search (BFS) demo

A small, dependency-free Python 3 demo of breadth-first search: level-order
traversal, shortest paths and distances in unweighted graphs, bipartite
testing, and a grid shortest-route search.

## What it shows

| Function | Purpose |
| --- | --- |
| `bfs_order(graph, start)` | BFS traversal; returns reachable vertices by distance |
| `bfs_levels(graph, start)` | Same traversal grouped into levels (`levels[i]` is distance `i`) |
| `shortest_distances(graph, start)` | Edge count of a shortest path to every reachable vertex |
| `bfs_path(graph, start, goal)` | A shortest path between two vertices, or `None` if unreachable |
| `is_bipartite(graph)` | Two-colouring check over all components |
| `shortest_path_grid(grid, start, goal)` | Shortest route through a 2D `"1"`/`"0"` grid |

A graph is a `dict[str, list[str]]` adjacency list, for example:

```python
graph = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"],
}
```

The search visits neighbours in adjacency-list order and marks a vertex as
soon as it is enqueued, so each reachable vertex is processed exactly once
and cycles terminate. Because vertices are processed in order of distance,
the first path found to a vertex is a shortest one.

Unlike DFS, `bfs_path` is guaranteed to return a path with the fewest edges.
On the sample graph, DFS happens to return `A -> B -> E -> F` (3 edges)
while BFS returns `A -> C -> F` (2 edges).

## Run the demo

```bash
cd bfs
python3 bfs.py
```

Output:

```text
Graph (undirected):
  A: B C
  B: A D E
  C: A F
  D: B
  E: B F
  F: C E

BFS order from A: A -> B -> C -> D -> E -> F
BFS levels: [['A'], ['B', 'C'], ['D', 'E', 'F']]
Distances from A: {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 2}

Shortest path A -> F: A -> C -> F (2 edges)
Bipartite: False

Grid ('1' = open, '0' = wall):
  1 1 1 0 1
  0 0 1 0 1
  1 1 1 1 1
  1 0 0 0 1
  1 1 1 1 1
Shortest route (0, 0) -> (0, 4): (0, 0) -> (0, 1) -> (0, 2) -> (1, 2) -> (2, 2) -> (2, 3) -> (2, 4) -> (1, 4) -> (0, 4) (8 moves)
```

The sample graph contains the odd cycle `A -> B -> E -> F -> C -> A`, so
`is_bipartite` correctly reports `False`; the tests also cover an even
cycle, a tree and disconnected components.

## Run the tests

The tests use only the standard library (`unittest`):

```bash
# from the repository root
python3 -m unittest discover -v

# or from this directory
cd bfs
python3 -m unittest -v
```

## Complexity

For a graph with `V` vertices and `E` edges, BFS is `O(V + E)` time and
`O(V)` space. The grid version is `O(rows * cols)` time and space.

## BFS vs DFS

Both searches visit every reachable vertex once, so both are `O(V + E)`.
The difference is the order:

- BFS uses a FIFO queue, explores in widening layers, and therefore finds
  shortest paths (fewest edges) in unweighted graphs.
- DFS uses a stack (or recursion), dives deep first, and uses less memory
  on wide graphs, but a path it finds is not necessarily the shortest.

Use BFS for shortest paths, level/round-based problems and bipartite
checks; use DFS for exhaustive traversal, backtracking and connectivity
checks where path length does not matter.
