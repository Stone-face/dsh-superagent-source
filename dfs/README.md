# Depth-first search (DFS) demo

A small, dependency-free Python 3 demo of depth-first search: the
recursive and iterative implementations, path finding, connected
components and a grid flood fill.

## What it shows

| Function | Purpose |
| --- | --- |
| `dfs_preorder(graph, start)` | Recursive DFS; returns visited vertices in preorder |
| `dfs_preorder_iterative(graph, start)` | Same order with an explicit stack; not limited by recursion depth |
| `dfs_path(graph, start, goal)` | One DFS path between two vertices, or `None` if unreachable |
| `connected_components(graph)` | Components of an undirected graph via repeated DFS |
| `count_islands(grid)` | Stack-based flood fill over a 2D `"1"`/`"0"` grid |

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

The search visits neighbours in adjacency-list order, skips vertices
already seen (so cycles terminate), and `connected_components` starts a
new search for every vertex not reached yet.

## Run the demo

```bash
cd dfs
python3 dfs.py
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

DFS preorder (recursive): A -> B -> D -> E -> F -> C
DFS preorder (iterative): A -> B -> D -> E -> F -> C
Same order: True

Path A -> F: A -> B -> E -> F
Connected components: [['A', 'B', 'D', 'E', 'F', 'C']]

Grid ('1' = land, '0' = water):
  1 1 0 0 0
  1 1 0 0 1
  0 0 1 0 1
  0 0 0 1 1
Number of islands: 3
```

## Run the tests

The tests use only the standard library (`unittest`, 20 tests):

```bash
# from the repository root
python3 -m unittest discover -v

# or from this directory
cd dfs
python3 -m unittest -v
```

## Complexity

For a graph with `V` vertices and `E` edges, DFS is `O(V + E)` time and
`O(V)` space. The grid version is `O(rows * cols)` time and space.

## Recursive vs iterative

`dfs_preorder` follows the textbook definition and is the easiest to
read, but Python's default recursion limit (`sys.getrecursionlimit()`,
1000) caps how deep it can go. `dfs_preorder_iterative` keeps the same
order using an explicit stack and is the better choice for large or
deep graphs.
