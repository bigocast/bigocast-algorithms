# Breadth-first search: print a tree

BigOCast | Moein

Print every node's label, finishing one level before the next. A queue remembers
the next turn: take a node from the front, print its label, and add its children
at the back.

## Run

Use Python 3.10 or newer. No third-party packages are needed. From the repository
root:

```sh
python3 trees/bfs/printing/print_bfs.py
python3 -m unittest discover -s trees/bfs/printing -v
```

The runner demonstrates four inputs:

```text
Five-node tree: A B C D E
Empty tree:
Single node: A
Wide tree: A B C D E F
```

`print_bfs` prints a space after every label, including the last one, and adds no
newline. The runner supplies headings and a final newline for each example.
The function returns `None`; it does not build a result list. An empty tree
prints nothing.

## Build the example

A `Node` has a label and an ordered list of children. Omitting the children gives
it its own empty list, making it a leaf.

```python
root = Node("A", [Node("B", [Node("D"), Node("E")]), Node("C")])
print_bfs(root)
```

```text
       A
     /   \
    B     C
   / \
  D   E
```

After printing A, the queue is `[B, C]`. Taking B out and adding its children
leaves `[C, D, E]`. C keeps its turn because it was already waiting. The exact
printed text is `"A B C D E "`.

## Contract and costs

Pass `None` or the root of a finite ordered tree. Every non-root node has one
parent, with no cycles or shared children. The caller guarantees this structure;
the function does not validate it or use a visited set. Labels are strings and
may repeat. Child-list order determines the traversal, not alphabetical order.
The input labels and child lists are unchanged.

For `n` nodes, each node enters and leaves the unbounded `deque` once, and the
child loops examine `n - 1` links in total. This is **O(n) traversal work**, plus
printing the labels. Counting characters, it is **O(n + L) time**, where `L` is
the total length of the labels, assuming constant work per written character.
An empty input takes O(1).

The queue needs **O(w) auxiliary space**, where `w` is the widest level. It can
contain parts of two consecutive levels: here the widest level has 2 nodes, but
the queue reaches 3 at `[C, D, E]`. There is no stored output list. The input tree
and any buffering performed by the output stream are separate from this queue
space bound.

The tests check exact stdout and return values, repeated labels, input
preservation, a 3,000-node chain, a 4,096-child root, and 520 generated trees
against an independent depth-bucket oracle. They also observe the actual queue
at the `[C, D, E]` checkpoint.

Try reversing A's children, giving two nodes the same label, or adding a child
beneath E. Predict the output before running it. Keep the finite-tree contract.

The earlier [BFS foundations example](../foundations/) remains available; that
variant returns a list instead of printing.
