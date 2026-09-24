"""Correctness checks for the BigOCast A* foundations example, by Moein."""

from collections import deque
from itertools import pairwise, product
from random import Random
import unittest
from unittest.mock import patch

import a_star as lesson


def breadth_first_cost(grid, start, goal):
    """An independent unit-cost oracle; do not use the A* neighbor helper."""
    queue = deque([(start, 0)])
    seen = {start}
    checked = 0
    while queue:
        (x, y), distance = queue.popleft()
        checked += 1
        if (x, y) == goal:
            return distance, checked
        for nx, ny in ((x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y)):
            cell = (nx, ny)
            if (
                0 <= ny < len(grid)
                and 0 <= nx < len(grid[0])
                and grid[ny][nx] == "."
                and cell not in seen
            ):
                seen.add(cell)
                queue.append((cell, distance + 1))
    return None, checked


class AStarTests(unittest.TestCase):
    def assert_shortest_legal_path(self, grid, start, goal):
        expected, _ = breadth_first_cost(grid, start, goal)
        path = lesson.a_star(grid, start, goal)
        self.assertEqual(None if path is None else len(path) - 1, expected)
        if path is not None:
            self.assertEqual((path[0], path[-1]), (start, goal))
            self.assertTrue(all(grid[y][x] == "." for x, y in path))
            self.assertTrue(
                all(abs(x - u) + abs(y - v) == 1 for (x, y), (u, v) in pairwise(path))
            )

    def test_exact_wall_route_from_video(self):
        self.assertEqual(
            lesson.a_star(lesson.GRID, lesson.START, lesson.GOAL),
            [(0, 1), (1, 1), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)],
        )

    def test_open_floor_route_and_comparison_counts(self):
        grid = (".....",) * 3
        # Count heap removals without adding instrumentation to the taught function.
        # This open map produces no stale entries, so each removal is a checked cell.
        with patch.object(lesson, "heappop", wraps=lesson.heappop) as pop:
            path = lesson.a_star(grid, lesson.START, lesson.GOAL)
        self.assertEqual(path, [(x, 1) for x in range(5)])
        self.assertEqual(pop.call_count, 5)
        self.assertEqual(breadth_first_cost(grid, lesson.START, lesson.GOAL), (4, 11))

    def test_start_is_goal(self):
        self.assertEqual(lesson.a_star((".",), (0, 0), (0, 0)), [(0, 0)])

    def test_unreachable_goal(self):
        self.assertIsNone(lesson.a_star((".#.",), (0, 0), (2, 0)))

    def test_single_row_and_column(self):
        for grid, goal in (((".....",), (4, 0)), ((".",) * 5, (0, 4))):
            with self.subTest(grid=grid):
                self.assert_shortest_legal_path(grid, (0, 0), goal)

    def test_exhaustive_three_by_three_maps(self):
        for walls in product(".#", repeat=7):
            cells = [".", *walls, "."]
            grid = tuple("".join(cells[i : i + 3]) for i in (0, 3, 6))
            with self.subTest(grid=grid):
                self.assert_shortest_legal_path(grid, (0, 0), (2, 2))

    def test_seeded_maps_and_arbitrary_endpoints(self):
        rng = Random(230923)
        for _ in range(300):
            width, height = rng.randint(1, 12), rng.randint(1, 12)
            cells = [["#" if rng.random() < 0.3 else "." for _ in range(width)] for _ in range(height)]
            start = (rng.randrange(width), rng.randrange(height))
            goal = (rng.randrange(width), rng.randrange(height))
            cells[start[1]][start[0]] = cells[goal[1]][goal[0]] = "."
            grid = tuple(map("".join, cells))
            with self.subTest(grid=grid, start=start, goal=goal):
                self.assert_shortest_legal_path(grid, start, goal)

    def test_invalid_inputs(self):
        cases = [
            ([], (0, 0), (0, 0)),
            ("...", (0, 0), (0, 0)),
            (("",), (0, 0), (0, 0)),
            ((1,), (0, 0), (0, 0)),
            (("..", "..."), (0, 0), (1, 0)),
            ((".x",), (0, 0), (1, 0)),
            (("..",), (-1, 0), (1, 0)),
            (("..",), (0, 0), (2, 0)),
            (("..",), [0, 0], (1, 0)),
            (("..",), (False, 0), (1, 0)),
            (("..",), (0, 0), (1.0, 0)),
            (("#.",), (0, 0), (1, 0)),
            ((".#",), (0, 0), (1, 0)),
        ]
        for grid, start, goal in cases:
            with self.subTest(grid=grid, start=start, goal=goal):
                with self.assertRaises(ValueError):
                    lesson.a_star(grid, start, goal)

    def test_input_is_not_modified(self):
        grid = list(lesson.GRID)
        original = grid.copy()
        lesson.a_star(grid, lesson.START, lesson.GOAL)
        self.assertEqual(grid, original)


if __name__ == "__main__":
    unittest.main()
