# A* foundations: a route around a wall

BigOCast | Moein

This is the complete Python implementation for **A* Search: Find a Route Around a
Wall**. It also runs the map used in **How A* Guides a Robot Around a Shelf** and
the open floor from **Why A* Checks Fewer Squares on This Map**.

Start with [a_star.py](a_star.py). It includes every helper needed to run the search.

## Run it

From the repository root, with Python 3.10 or newer:

```sh
python3 graphs/a_star/foundations/a_star.py
```

No third-party packages are required. The output is:

```text
Route around a wall
Path: [(0, 1), (1, 1), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)]
Moves: 6

Open floor
Path: [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)]
Moves: 4
```

## Map and contract

The wall example uses this grid:

```text
.....
S.#.G
.....
```

In Python, store only `.` for an open square and `#` for a wall. Pass the start and
goal separately as `(column, row)` tuples, with zero-based coordinates. Here they
are `(0, 1)` and `(4, 1)`.

`a_star(grid, start, goal)` accepts a nonempty list or tuple of equal-length strings.
Both endpoints must be open squares. Coordinates must contain integers, not booleans.
Invalid input raises `ValueError`.

Moves go up, down, left, or right. Every move costs one. The result is a list of
coordinates from start to goal, including both endpoints, or `None` if no route
exists. When start equals goal, the result contains that one square and costs zero
moves. The input grid is never modified.

## Follow the decisions

1. Keep the cheapest known cost to each square in `best`.
2. Use Manhattan distance, the horizontal plus vertical distance to the goal, as
   the remaining estimate. It ignores walls but never overestimates the number of
   legal moves needed under this movement contract.
3. Choose the smallest estimated total: cost so far plus remaining estimate.
4. When a cheaper route reaches a neighbor, update its cost and parent and add a
   new heap entry. Skip an older entry if its saved cost is no longer current.
5. Stop when a current goal entry is removed from the heap. Follow the parent
   links backward, then reverse them to recover the route.

The neighbor order is right, up, down, then left. Heap entries compare estimated
total, remaining estimate, cost so far, then `(column, row)`. These tie rules make
the demonstrated route reproducible; other valid tie rules can find another
equally short route.

The open-floor Short counts checked squares, including start and goal. Its
nearest-first breadth-first search checks eleven squares; this A* search checks
five. Both routes have four moves. The tests reproduce those counts with the
specified ordering. A* does not always check fewer squares on every map.

## Try changing the input

- Change the wall grid to `(".....", ".....", ".....")`. The direct route takes four moves.
- Change it to `("..#..", "..#..", "..#..")`. With the same endpoints, no route exists.
- Set `GOAL = START`. The route contains one position and takes zero moves.
- Move a wall or the destination, then predict the route before running the code.

Keep movement four-way and costs equal to one. Diagonal moves, weighted terrain,
or a different estimate require revisiting the algorithm's assumptions.

## Cost

Let `N` be the number of input squares and `L` the number of positions in the
returned route. Validation reads the grid in `O(N)` time. Each square has at most
four neighbors. Manhattan distance is consistent for these moves, so processing
a current square establishes its final shortest cost; the bounded number of edges
limits heap insertions, including obsolete entries, to `O(N)`.

The worst-case running time is `O(N log N)`, with `O(N)` auxiliary space for the
heap, costs, and parents. Reconstructing the route takes `O(L)` time and uses
`O(L)` output space; the reverse copy also temporarily uses `O(L)` space, within
the overall `O(N)` auxiliary bound. The caller's input grid is separate.

## Check correctness

```sh
python3 -m unittest discover -s graphs/a_star/foundations -v
```

The tests check the exact video examples, invalid input, an unreachable goal,
equal endpoints, narrow maps, every placement of the seven optional walls on a
3-by-3 map, and 300 reproducible random maps. An independent breadth-first search
checks shortest costs; the tests also verify that returned paths use legal moves.
