"""BigOCast | Moein: breadth-first traversal of an ordered rooted tree.

The caller supplies a finite tree: every non-root node has one parent, children
are Nodes in a fixed order, and there are no cycles or shared child nodes.
Labels are names, not sort keys, and distinct nodes may have the same label.
The function does not validate the shape or mutate the input.

For n nodes and widest level w, bfs takes O(n) time and O(w) auxiliary queue
space. The queue can straddle two levels; its exact peak need not equal w.
The returned list uses O(n) output space. Input construction and the separate
verification/parity helpers are outside those traversal costs.
"""

from __future__ import annotations

import json
from collections import deque
from dataclasses import dataclass, field


@dataclass(eq=False)
class Node:
    label: str
    children: list[Node] = field(default_factory=list)


def bfs(root: Node | None) -> list[str]:
    """Return labels in level order."""
    if root is None:
        return []
    order = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        order.append(node.label)
        for child in node.children:
            queue.append(child)
    return order


def main_tree() -> Node:
    return Node(
        "A",
        [
            Node("B", [Node("D"), Node("E")]),
            Node("C", [Node("F"), Node("G")]),
        ],
    )


def levels_short_tree() -> Node:
    return Node("R", [Node("Z", [Node("M")]), Node("B", [Node("C")])])


def queue_short_tree() -> Node:
    return Node("A", [Node("B", [Node("D"), Node("E")]), Node("C")])


def _case_roots() -> list[Node | None]:
    return [
        main_tree(),
        levels_short_tree(),
        queue_short_tree(),
        None,
        Node("solo"),
        Node("R", [Node("B", [Node("D", [Node("F")])]), Node("C", [Node("E")])]),
        Node("X", [Node("X"), Node("X", [Node("X")])]),
        Node("R", [Node("Z"), Node("A"), Node("M"), Node("B")]),
    ]


def _tree_data(root: Node | None):
    """Serialize small parity examples only; this is not part of bfs."""
    if root is None:
        return None
    return {"label": root.label, "children": [_tree_data(child) for child in root.children]}


def parity_cases():
    """Browser field `tree` is nested JSON {label, children}, or null for empty."""
    return [
        {
            "input": {"tree": json.dumps(_tree_data(root))},
            "expected": {"order": bfs(root)},
        }
        for root in _case_roots()
    ]


def verify():
    """Small executable lesson facts; test_algorithm.py adds independent oracles."""
    expected = [
        ["A", "B", "C", "D", "E", "F", "G"],
        ["R", "Z", "B", "M", "C"],
        ["A", "B", "C", "D", "E"],
        [],
        ["solo"],
        ["R", "B", "C", "D", "E", "F"],
        ["X", "X", "X", "X"],
        ["R", "Z", "A", "M", "B"],
    ]
    actual = [bfs(root) for root in _case_roots()]
    assert actual == expected
    return {
        "checked": len(expected),
        "example": actual[0],
        "short_levels": actual[1],
        "short_queue": actual[2],
        "empty": actual[3],
    }


if __name__ == "__main__":
    verify()
    for name, build in (
        ("Main", main_tree),
        ("Read the levels", levels_short_tree),
        ("Keep the next turn", queue_short_tree),
    ):
        print(f"{name}: {' '.join(bfs(build()))}")
