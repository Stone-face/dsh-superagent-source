"""Tests for the BFS demo. Run with ``python3 -m unittest -v``."""
import unittest

from bfs import (
    SAMPLE_GRAPH,
    SAMPLE_GRID,
    bfs_levels,
    bfs_order,
    bfs_path,
    is_bipartite,
    shortest_distances,
    shortest_path_grid,
)


class BfsOrderTests(unittest.TestCase):
    def test_sample_order(self):
        self.assertEqual(
            bfs_order(SAMPLE_GRAPH, "A"),
            ["A", "B", "C", "D", "E", "F"],
        )

    def test_cycle_visits_each_vertex_once(self):
        order = bfs_order(SAMPLE_GRAPH, "A")
        self.assertEqual(len(order), len(set(order)))

    def test_disconnected_vertices_are_not_reached(self):
        graph = {"A": ["B"], "B": ["A"], "C": ["D"], "D": ["C"]}
        self.assertEqual(bfs_order(graph, "A"), ["A", "B"])

    def test_single_vertex(self):
        self.assertEqual(bfs_order({"A": []}, "A"), ["A"])

    def test_directed_edges_are_followed_one_way(self):
        graph = {"A": ["B"], "B": ["C"], "C": []}
        self.assertEqual(bfs_order(graph, "A"), ["A", "B", "C"])
        self.assertEqual(bfs_order(graph, "B"), ["B", "C"])

    def test_unknown_start_raises(self):
        with self.assertRaises(ValueError):
            bfs_order(SAMPLE_GRAPH, "Z")


class BfsLevelsTests(unittest.TestCase):
    def test_sample_levels(self):
        self.assertEqual(
            bfs_levels(SAMPLE_GRAPH, "A"),
            [["A"], ["B", "C"], ["D", "E", "F"]],
        )

    def test_levels_flatten_to_bfs_order(self):
        self.assertEqual(
            [v for level in bfs_levels(SAMPLE_GRAPH, "A") for v in level],
            bfs_order(SAMPLE_GRAPH, "A"),
        )

    def test_unknown_start_raises(self):
        with self.assertRaises(ValueError):
            bfs_levels(SAMPLE_GRAPH, "Z")


class ShortestDistancesTests(unittest.TestCase):
    def test_sample_distances(self):
        self.assertEqual(
            shortest_distances(SAMPLE_GRAPH, "A"),
            {"A": 0, "B": 1, "C": 1, "D": 2, "E": 2, "F": 2},
        )

    def test_start_is_zero(self):
        self.assertEqual(shortest_distances({"A": []}, "A"), {"A": 0})

    def test_unreachable_vertices_are_omitted(self):
        graph = {"A": ["B"], "B": ["A"], "C": ["D"], "D": ["C"]}
        self.assertEqual(shortest_distances(graph, "A"), {"A": 0, "B": 1})

    def test_unknown_start_raises(self):
        with self.assertRaises(ValueError):
            shortest_distances(SAMPLE_GRAPH, "Z")


class BfsPathTests(unittest.TestCase):
    def test_returns_shortest_path(self):
        self.assertEqual(bfs_path(SAMPLE_GRAPH, "A", "F"), ["A", "C", "F"])

    def test_start_equals_goal(self):
        self.assertEqual(bfs_path(SAMPLE_GRAPH, "A", "A"), ["A"])

    def test_returns_none_when_unreachable(self):
        graph = {"A": ["B"], "B": ["A"], "C": []}
        self.assertIsNone(bfs_path(graph, "A", "C"))

    def test_path_is_a_valid_walk(self):
        path = bfs_path(SAMPLE_GRAPH, "A", "D")
        self.assertEqual(path, ["A", "B", "D"])
        for current, following in zip(path, path[1:]):
            self.assertIn(following, SAMPLE_GRAPH[current])

    def test_path_length_equals_shortest_distance(self):
        distances = shortest_distances(SAMPLE_GRAPH, "A")
        for goal, distance in distances.items():
            path = bfs_path(SAMPLE_GRAPH, "A", goal)
            self.assertIsNotNone(path)
            self.assertEqual(len(path) - 1, distance)

    def test_unknown_start_raises(self):
        with self.assertRaises(ValueError):
            bfs_path(SAMPLE_GRAPH, "Z", "A")


class BipartiteTests(unittest.TestCase):
    def test_sample_odd_cycle_is_not_bipartite(self):
        # A-B-E-F-C-A is a 5-cycle, so two colours cannot work.
        self.assertFalse(is_bipartite(SAMPLE_GRAPH))

    def test_even_cycle_is_bipartite(self):
        graph = {
            "A": ["B", "D"],
            "B": ["A", "C"],
            "C": ["B", "D"],
            "D": ["A", "C"],
        }
        self.assertTrue(is_bipartite(graph))

    def test_triangle_is_not_bipartite(self):
        graph = {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}
        self.assertFalse(is_bipartite(graph))

    def test_tree_is_bipartite(self):
        graph = {"A": ["B", "C"], "B": ["A"], "C": ["A"]}
        self.assertTrue(is_bipartite(graph))

    def test_odd_cycle_in_disconnected_part_is_detected(self):
        graph = {
            "A": ["B"],
            "B": ["A"],
            "C": ["D", "E"],
            "D": ["C", "E"],
            "E": ["C", "D"],
        }
        self.assertFalse(is_bipartite(graph))

    def test_disconnected_even_components_are_bipartite(self):
        graph = {"A": ["B"], "B": ["A"], "C": ["D"], "D": ["C"]}
        self.assertTrue(is_bipartite(graph))

    def test_self_loop_is_not_bipartite(self):
        self.assertFalse(is_bipartite({"A": ["A"]}))


class ShortestPathGridTests(unittest.TestCase):
    def test_sample_route(self):
        route = shortest_path_grid(SAMPLE_GRID, (0, 0), (0, 4))
        self.assertEqual(
            route,
            [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2),
             (2, 3), (2, 4), (1, 4), (0, 4)],
        )
        self.assertEqual(len(route) - 1, 8)

    def test_route_steps_are_adjacent_and_walkable(self):
        route = shortest_path_grid(SAMPLE_GRID, (0, 0), (4, 0))
        self.assertIsNotNone(route)
        for (row, col), (next_row, next_col) in zip(route, route[1:]):
            self.assertEqual(abs(row - next_row) + abs(col - next_col), 1)
            self.assertEqual(SAMPLE_GRID[next_row][next_col], "1")

    def test_walls_can_make_goal_unreachable(self):
        grid = [["1", "0"], ["0", "1"]]
        self.assertIsNone(shortest_path_grid(grid, (0, 0), (1, 1)))

    def test_start_equals_goal(self):
        self.assertEqual(
            shortest_path_grid(SAMPLE_GRID, (2, 2), (2, 2)),
            [(2, 2)],
        )

    def test_cell_outside_grid_raises(self):
        with self.assertRaises(ValueError):
            shortest_path_grid(SAMPLE_GRID, (0, 0), (5, 0))

    def test_wall_endpoint_raises(self):
        with self.assertRaises(ValueError):
            shortest_path_grid(SAMPLE_GRID, (0, 3), (0, 4))

    def test_ragged_grid_is_rejected(self):
        with self.assertRaises(ValueError):
            shortest_path_grid([["1"], ["1", "0"]], (0, 0), (0, 0))

    def test_does_not_modify_input(self):
        grid = [row[:] for row in SAMPLE_GRID]
        shortest_path_grid(grid, (0, 0), (0, 4))
        self.assertEqual(grid, SAMPLE_GRID)


if __name__ == "__main__":
    unittest.main()
