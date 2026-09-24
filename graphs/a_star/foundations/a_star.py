"""A* foundations: four-way movement, unit costs, and Manhattan distance.

BigOCast | Moein
Companion to "A* Search: Find a Route Around a Wall".
Coordinates are (column, row). Run this file for the wall and open-floor examples.
"""

from heapq import heappop, heappush
from math import inf

GRID = (".....", "..#..", ".....")
START, GOAL = (0, 1), (4, 1)


def validate_grid(grid, start, goal):
    """Require a rectangular .# grid and two open integer-coordinate cells."""
    if not isinstance(grid, (list, tuple)) or not grid:
        raise ValueError("Use a nonempty grid.")
    if any(not isinstance(row, str) for row in grid):
        raise ValueError("Grid rows must be text.")
    width = len(grid[0])
    if width < 1 or any(len(row) != width for row in grid):
        raise ValueError("Use equal, nonempty row widths.")
    if any(char not in ".#" for row in grid for char in row):
        raise ValueError("Use only . for open cells and # for walls.")
    for cell in (start, goal):
        if (
            not isinstance(cell, tuple)
            or len(cell) != 2
            or any(type(value) is not int for value in cell)
            or not 0 <= cell[0] < width
            or not 0 <= cell[1] < len(grid)
        ):
            raise ValueError("Start and goal must be valid column,row coordinates.")
        if grid[cell[1]][cell[0]] == "#":
            raise ValueError("Start and goal must be on open cells.")


def manhattan(cell, goal):
    """Estimate the moves left by ignoring walls and counting across plus down/up."""
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def neighbors(grid, cell):
    """Yield legal neighbors in the video's order: right, up, down, then left."""
    x, y = cell
    for nxt in ((x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y)):
        nx, ny = nxt
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] == ".":
            yield nxt


def build_path(parent, goal):
    """Follow saved parent links backward, then return the start-to-goal order."""
    path = [goal]
    while path[-1] in parent:
        path.append(parent[path[-1]])
    return path[::-1]


def a_star(grid, start, goal):
    """Return a shortest path, including both endpoints, or None if unreachable.

    Invalid input raises ValueError. Heap ties use remaining estimate, cost so
    far, then coordinates after comparing estimated total cost.
    """
    validate_grid(grid, start, goal)
    best = {start: 0}
    parent = {}
    remaining = manhattan(start, goal)
    frontier = [(remaining, remaining, 0, start)]
    while frontier:
        _, _, cost, cell = heappop(frontier)
        # A later discovery may have made this older queue entry obsolete.
        if cost != best[cell]:
            continue
        if cell == goal:
            return build_path(parent, goal)
        for nxt in neighbors(grid, cell):
            candidate = cost + 1
            if candidate < best.get(nxt, inf):
                best[nxt] = candidate
                parent[nxt] = cell
                remaining = manhattan(nxt, goal)
                entry = (
                    candidate + remaining,
                    remaining,
                    candidate,
                    nxt,
                )
                heappush(frontier, entry)
    return None


if __name__ == "__main__":
    for name, grid in (("Route around a wall", GRID), ("Open floor", (".....",) * 3)):
        path = a_star(grid, START, GOAL)
        print(name)
        print("Path:", path)
        print("Moves:", None if path is None else len(path) - 1)
        print()
