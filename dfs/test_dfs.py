"""Tests for the DFS demo. Run with ``python3 -m unittest -v``."""
import unittest

from dfs import (
    SAMPLE_GRAPH,
    SAMPLE_GRID,
    connected_components,
    count_islands,
    dfs_path,
    dfs_preorder,
    dfs_preorder_iterative,
)


class DfsPreorderTests(unittest.TestCase):
    def test_recursive_order(self):
        self.assertEqual(
            dfs_preorder(SAMPLE_GRAPH, "A"),
            ["A", "B", "D", "E", "F", "C"],
        )

    def test_iterative_matches_recursive(self):
        self.assertEqual(
            dfs_preorder_iterative(SAMPLE_GRAPH, "A"),
            dfs_preorder(SAMPLE_GRAPH, "A"),
        )

    def test_cycle_visits_each_vertex_once(self):
        order = dfs_preorder(SAMPLE_GRAPH, "A")
        self.assertEqual(len(order), len(set(order)))

    def test_disconnected_vertices_are_not_reached(self):
        graph = {"A": ["B"], "B": ["A"], "C": ["D"], "D": ["C"]}
        self.assertEqual(dfs_preorder(graph, "A"), ["A", "B"])

    def test_single_vertex(self):
        self.assertEqual(dfs_preorder({"A": []}, "A"), ["A"])

    def test_unknown_start_raises(self):
        with self.assertRaises(ValueError):
            dfs_preorder(SAMPLE_GRAPH, "Z")
        with self.assertRaises(ValueError):
            dfs_preorder_iterative(SAMPLE_GRAPH, "Z")


class DfsPathTests(unittest.TestCase):
    def test_finds_path(self):
        self.assertEqual(
            dfs_path(SAMPLE_GRAPH, "A", "F"),
            ["A", "B", "E", "F"],
        )

    def test_start_equals_goal(self):
        self.assertEqual(dfs_path(SAMPLE_GRAPH, "A", "A"), ["A"])

    def test_returns_none_when_unreachable(self):
        graph = {"A": ["B"], "B": ["A"], "C": []}
        self.assertIsNone(dfs_path(graph, "A", "C"))

    def test_unknown_start_raises(self):
        with self.assertRaises(ValueError):
            dfs_path(SAMPLE_GRAPH, "Z", "A")

    def test_path_is_a_valid_walk(self):
        path = dfs_path(SAMPLE_GRAPH, "A", "D")
        self.assertEqual(path, ["A", "B", "D"])
        for current, following in zip(path, path[1:]):
            self.assertIn(following, SAMPLE_GRAPH[current])


class ConnectedComponentsTests(unittest.TestCase):
    def test_single_component(self):
        self.assertEqual(
            connected_components(SAMPLE_GRAPH),
            [["A", "B", "D", "E", "F", "C"]],
        )

    def test_disconnected_graph(self):
        graph = {"A": ["B"], "B": ["A"], "C": ["D"], "D": ["C"], "E": []}
        self.assertEqual(
            connected_components(graph),
            [["A", "B"], ["C", "D"], ["E"]],
        )


class CountIslandsTests(unittest.TestCase):
    def test_sample_grid(self):
        self.assertEqual(count_islands(SAMPLE_GRID), 3)

    def test_empty_grid(self):
        self.assertEqual(count_islands([]), 0)

    def test_all_water(self):
        self.assertEqual(count_islands([["0", "0"], ["0", "0"]]), 0)

    def test_single_cell(self):
        self.assertEqual(count_islands([["1"]]), 1)

    def test_diagonal_cells_are_separate(self):
        self.assertEqual(count_islands([["1", "0"], ["0", "1"]]), 2)

    def test_does_not_modify_input(self):
        grid = [row[:] for row in SAMPLE_GRID]
        count_islands(grid)
        self.assertEqual(grid, SAMPLE_GRID)

    def test_ragged_grid_is_rejected(self):
        with self.assertRaises(ValueError):
            count_islands([["1"], ["1", "0"]])


if __name__ == "__main__":
    unittest.main()
