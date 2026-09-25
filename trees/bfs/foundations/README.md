# Breadth-first search: tree foundations

BigOCast | Moein

Read every node in a tree, finishing one level before moving to the next. A queue
remembers whose turn comes next: remove from the front, record the node's label,
then add its children at the back.

This folder contains the complete Python implementation and all three examples
from the long lesson and its two Shorts. No third-party packages are required.

## Run

Use Python 3.10 or newer. From the repository root:

```sh
python3 trees/bfs/foundations/bfs.py
python3 -m unittest discover -s trees/bfs/foundations -v
```

Expected example output:

```text
Main: A B C D E F G
Read the levels: R Z B M C
Keep the next turn: A B C D E
```

The 13 tests include exact examples, empty and uneven trees, repeated labels,
input preservation, a 5,000-node chain, a 4,096-child root, and 520 reproducible
generated cases checked against an independent depth-bucket oracle. They also
observe the actual BFS queue to check insertion counts and peak size.

## Tree contract

`bfs(root)` accepts `None` or a `Node` that is the root of an already constructed
finite ordered tree. Each node has a string `label` and an ordered list of child
`Node` references. A leaf has an empty child list.

- Each non-root node has exactly one parent. There are no cycles or shared child
  nodes. The caller guarantees this shape; the function does not validate it.
- Child-list order determines sibling order. Labels are names, not sort keys, and
  different nodes may have equal labels.
- The result is a new flat list of labels in level order. `None` returns `[]`.
- The function does not change labels or child lists.

The queue has no capacity limit. The tree is an input to the traversal, so it is
constructed before calling `bfs`.

## The three examples

The long lesson uses `main_tree()`:

```text
        A             level 0
      /   \
     B     C          level 1
    / \   / \
   D   E F   G        level 2
```

A level counts links from the root. Visiting a node means recording its label.
The root A has direct children B and C; D is a child of B. After visiting A, the
queue is `[B, C]`. B's children join behind C, leaving `[C, D, E]`. Processing C
then produces `[D, E, F, G]`. Finishing those leaves empties the queue and returns
`["A", "B", "C", "D", "E", "F", "G"]`.

The first Short uses `levels_short_tree()`:

```text
       R
     /   \
    Z     B
    |     |
    M     C
```

The complete traversal is `R, Z, B, M, C`. The deliberately unsorted labels make
it clear that the tree's levels and child order determine the result.

The second Short uses `queue_short_tree()`:

```text
       A
     /   \
    B     C
   / \
  D   E
```

After B is processed, the queue is `[C, D, E]`: C was already waiting. The complete
traversal is `A, B, C, D, E`, and the queue ends empty.

## Why the costs are O(n) and O(w)

Let `n` be the number of input nodes and `w` the largest number of nodes on any
one level.

Each node enters the queue once and leaves it once. The root is inserted during
initialization; the other `n - 1` insertions follow child links. Across the entire
traversal, the inner loop examines exactly `n - 1` child links, not `n` links for
every node. Constant-time deque end operations and amortized constant-time result
appends give **O(n) time** for a nonempty tree. An empty input takes O(1).

The queue contains parts of at most two consecutive levels, so it needs **O(w)
auxiliary space**. Its exact peak can exceed `w`: the second Short has widest
level 2 but a peak queue of 3 at `[C, D, E]`. The long example has width 4 and peak
queue 4.

The returned list stores `n` label references and uses **O(n) output space**.
Including that output, total additional storage is O(n). The supplied tree is
separate input storage. `verify()` and the small recursive JSON fixture helpers
are separate from `bfs`; their work is not included in these traversal costs.

## Try a change

- Reverse A's child list in `main_tree()` and predict the complete new order.
- Give two different nodes the same label. Both nodes still get visited.
- Add a child beneath a leaf and check that it waits until earlier levels finish.
- Compare a long chain with a wide root: both visit every node, but their queue
  sizes differ.

Keep the finite-tree contract when changing links. The lesson is a rooted-tree
traversal, so it does not include general-graph validation or a discovered set.
