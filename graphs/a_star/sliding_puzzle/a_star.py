"""BigOCast | Moein: A* Search: Solve a Sliding Puzzle.

One state is a whole three-by-three board; zero is its single empty space.
Run this file for the four-move lesson and both Shorts' three- and two-move examples.
The a_star entry point validates input; the small board helpers expect an
already validated board.
"""

import re
from heapq import heappop, heappush
from itertools import count

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
START = (1, 2, 3, 5, 0, 6, 4, 7, 8)
ESTIMATE_EXAMPLE = (1, 2, 3, 4, 8, 5, 7, 0, 6)
TWO_MOVE_EXAMPLE = (1, 2, 3, 4, 5, 6, 0, 7, 8)


# Normalize the caller's iterable once; lower-level helpers assume a valid board.
def validate_board(board):
    board = tuple(board)
    if (
        len(board) != 9
        or any(type(tile) is not int for tile in board)
        or set(board) != set(range(9))
    ):
        raise ValueError("Use each integer from 0 to 8 exactly once.")
    return board


# Each move slides one numbered tile. Do not also count the blank's distance.
def manhattan(board):
    total = 0
    for index, tile in enumerate(board):
        if tile == 0:
            continue
        row, col = divmod(index, 3)
        goal_row, goal_col = divmod(tile - 1, 3)
        total += abs(row - goal_row) + abs(col - goal_col)
    return total


# Directions describe the blank's movement; each yielded board is an immutable tuple.
def neighbors(board):
    blank = board.index(0)
    row, col = divmod(blank, 3)
    for dr, dc in ((-1, 0), (0, -1), (0, 1), (1, 0)):
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            other = 3 * nr + nc
            moved = list(board)
            moved[blank], moved[other] = (
                moved[other], moved[blank]
            )
            yield tuple(moved)


def solvable(board):
    """For this odd-width board and fixed goal, inversion parity must be even."""
    tiles = [tile for tile in board if tile != 0]
    inversions = sum(a > b for i, a in enumerate(tiles) for b in tiles[i + 1:])
    return inversions % 2 == 0


# The parent map must lead from this board back to a start whose parent is None.
def build_path(parent, board):
    path = []
    while board is not None:
        path.append(board)
        board = parent[board]
    path.reverse()
    return path


# Heap priority is estimated total, remaining estimate, then insertion order.
def a_star(start):
    start = validate_board(start)
    if not solvable(start):
        return None
    best = {start: 0}
    parent = {start: None}
    serial = count()
    h = manhattan(start)
    frontier = [(h, h, next(serial), 0, start)]
    while frontier:
        _, _, _, cost, board = heappop(frontier)
        if cost != best[board]:
            continue
        if board == GOAL:
            return build_path(parent, board)
        for nxt in neighbors(board):
            candidate = cost + 1
            if candidate < best.get(nxt, float("inf")):
                best[nxt] = candidate
                parent[nxt] = board
                h = manhattan(nxt)
                entry = (candidate + h, h, next(serial), candidate, nxt)
                heappush(frontier, entry)
    return None


# Optional text input: ASCII spaces, commas and slashes separate the nine digits.
def parse_input(text):
    if not isinstance(text, str) or len(text) > 100:
        raise ValueError("Enter nine digits using spaces, commas or slashes.")
    words = re.split(r"[ ,/]+", text.strip(" "))
    if len(words) != 9 or any(not re.fullmatch(r"[0-8]", word) for word in words):
        raise ValueError("Enter nine digits using spaces, commas or slashes.")
    return validate_board(tuple(map(int, words)))


if __name__ == "__main__":
    for name, start in (
        ("Four-move puzzle", START),
        ("Three-move estimate example", ESTIMATE_EXAMPLE),
        ("Two-move tile example", TWO_MOVE_EXAMPLE),
    ):
        path = a_star(start)
        print(name)
        print("Initial Manhattan estimate:", manhattan(start))
        print("Fewest moves:", None if path is None else len(path) - 1)
        if path is not None:
            for step, board in enumerate(path):
                rows = [
                    " ".join(str(tile) if tile else "_" for tile in board[row:row + 3])
                    for row in (0, 3, 6)
                ]
                print(f"{step}: {' / '.join(rows)}")
        print()
