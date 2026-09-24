# A* Search: Solve a Sliding Puzzle

BigOCast | Moein

Find a shortest sequence of slides for the classic 3-by-3 puzzle. This companion
contains the complete search from the long lesson and its four-move board, plus
the three-move and two-move boards from the two Shorts. For the earlier
grid-pathfinding lesson, see
[A* foundations](../foundations/).

## Run all three examples

Use Python 3.10 or newer. No third-party packages are required. From the repository root:

```sh
python3 graphs/a_star/sliding_puzzle/a_star.py
```

Start with [a_star.py](a_star.py). It prints every board in each shortest solution.
Slashes separate rows, and `_` displays the empty space:

```text
Four-move puzzle
Initial Manhattan estimate: 4
Fewest moves: 4
0: 1 2 3 / 5 _ 6 / 4 7 8
1: 1 2 3 / _ 5 6 / 4 7 8
2: 1 2 3 / 4 5 6 / _ 7 8
3: 1 2 3 / 4 5 6 / 7 _ 8
4: 1 2 3 / 4 5 6 / 7 8 _

Three-move estimate example
Initial Manhattan estimate: 3
Fewest moves: 3
0: 1 2 3 / 4 8 5 / 7 _ 6
1: 1 2 3 / 4 _ 5 / 7 8 6
2: 1 2 3 / 4 5 _ / 7 8 6
3: 1 2 3 / 4 5 6 / 7 8 _

Two-move tile example
Initial Manhattan estimate: 2
Fewest moves: 2
0: 1 2 3 / 4 5 6 / _ 7 8
1: 1 2 3 / 4 5 6 / 7 _ 8
2: 1 2 3 / 4 5 6 / 7 8 _
```

In the second Short's `TWO_MOVE_EXAMPLE`, tile `7` slides left into the blank,
then tile `8` slides left to finish the puzzle. The returned path includes all
three boards: the start, the board after sliding `7`, and the goal.

## Board and return contract

One search state is the entire board. Store its cells row by row in a tuple or
list, using `0` for the empty space:

```text
Start       Goal
1 2 3       1 2 3
5 _ 6       4 5 6
4 7 8       7 8 _
```

`a_star(start)` accepts a finite iterable containing each integer from `0` to `8`
exactly once, in row order. It converts that input to an immutable tuple. Invalid
contents or length raise `ValueError`; booleans and floats are not accepted as
integer tiles. A noniterable object is outside this contract and raises `TypeError`.
The caller's list is not modified.

A move swaps the empty space with one horizontally or vertically adjacent tile.
Every move costs one. The goal is fixed at `(1, 2, 3, 4, 5, 6, 7, 8, 0)`.
The result is a list of board tuples from the start to that goal, including both
endpoints. Its move count is `len(path) - 1`. A solved input returns `[GOAL]`;
a valid but unsolvable input returns `None`.

This implementation is specifically for a 3-by-3 board and this goal arrangement.
Changing the dimensions or goal also requires changing the helpers and the
solvability rule.

## Follow the search

1. Check inversion parity before searching. Ignore the blank and count pairs of
   numbered tiles that appear in the opposite order from the goal. For this
   odd-width puzzle, an odd count means the goal cannot be reached.
2. Keep the cheapest known move count `g` for each board in `best`.
3. Compute `h`, the sum of every numbered tile's horizontal and vertical distances
   from its goal position. Exclude the blank. Each slide moves just one numbered
   tile by one square, so this sum is a lower bound on the remaining moves.
4. Remove a board with the smallest `f = g + h` from the heap. On a tie, prefer
   smaller `h`, then earlier insertion. Neighbor generation moves the blank up,
   left, right, then down, skipping directions that leave the board.
5. For each neighbor, save a cheaper cost and its parent when found. Add a new heap
   entry for that improvement; skip an old entry if its stored cost is no longer
   the best cost for that board.
6. Stop when a current goal entry is removed from the heap. Follow its parents
   backward and reverse the list to recover the whole solution.

Manhattan distance is consistent here: one legal slide changes the estimate by
exactly one. A current board removed from the heap therefore has its final shortest
cost, and stopping at the goal returns a shortest solution. The tie rules make
the selected solution reproducible. Other valid tie rules can select another
equally short solution.

## Helper preconditions

Call `a_star` for a complete validated search. When using helpers directly:

- `validate_board(board)` validates and returns a tuple under the input contract above.
- `manhattan(board)`, `neighbors(board)` and `solvable(board)` expect an already
  validated board, such as the tuple returned by `validate_board`. They do not
  repeat validation. `neighbors` yields new board tuples and leaves its input alone.
- `build_path(parent, board)` expects a complete, acyclic parent chain. Every board
  on that chain must be a key in `parent`, and the start must map to `None`.
- `parse_input(text)` is an optional text helper. Use nine ASCII digits separated
  by spaces, commas or slashes, for example `"1 2 3 / 5 0 6 / 4 7 8"`. The text may
  contain at most 100 characters. Tabs and newlines are not separators. Invalid
  text or tile contents raise `ValueError`.

## Cost

Let `N` be the number of distinct board configurations discovered during the
search, and `L` the number of boards in the returned solution. `N` counts whole
boards, not the nine cells in one board. For this fixed puzzle, the reachable
component contains at most 181,440 configurations.

Each board contains exactly nine cells. Validation, inversion counting, calculating
the estimate, hashing or comparing a board, and making one neighbor therefore take
constant time in this search-state model. Use the usual constant-time dictionary
lookup model. A board has at most four neighbors. Consistency means each current
board is expanded at most once, so there are `O(N)` neighbor examinations and heap
insertions, including entries later made obsolete. Each heap operation costs at
most `O(log N)`.

The search takes `O(N log N)` time and `O(N)` auxiliary space for its heap, best
costs, parents and board tuples. Constructing the result adds `O(L)` time and
`O(L)` output storage; the result list refers to immutable board tuples, and its
reversal is in place. The input board is separate. An already solved or
parity-rejected valid board takes constant work.

These bounds describe work over the state graph of the fixed 3-by-3 puzzle. They
are not bounds in the number of tiles for a variable-size puzzle.

## Try changing a board

- Set `START = GOAL`. The solution has zero moves and one board.
- Use `START = (1, 2, 3, 4, 5, 6, 7, 0, 8)`. One slide reaches the goal.
- Swap `7` and `8` in the goal. That valid board is unsolvable and returns `None`.
- Try another board through `a_star(parse_input("1 2 3 / 4 0 6 / 7 5 8"))`.
- Before running a new board, predict its Manhattan estimate. It can be smaller
  than the true remaining distance even though it is exact in these three examples.

## Check correctness

```sh
python3 -m unittest discover -s graphs/a_star/sliding_puzzle -v
```

The tests construct an independent breadth-first oracle using its own legal-move
enumeration. They check all 181,440 reachable boards for correct successors,
admissible Manhattan estimates and consistency, and every one of the 362,880 board
permutations for agreement between inversion parity and reachability.

A* paths are checked against the oracle at one representative board per shortest
distance from 0 through 31 moves, plus the exact lesson examples. The tests also
cover solved and impossible boards, invalid input, text parsing and preservation of
the caller's list. They do not run A* separately from every possible starting board.
