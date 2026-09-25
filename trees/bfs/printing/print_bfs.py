"""BigOCast | Moein: print an ordered tree one level at a time.

The caller supplies a finite rooted tree with no cycles or shared children.
Children are already in the desired order; labels are names, not sort keys.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field


@dataclass(eq=False)
class Node:
    label: str
    children: list[Node] = field(default_factory=list)


def print_bfs(root):
    if root is None:
        return
    queue = deque([root])
    while queue:
        node = queue.popleft()
        print(node.label, end=" ")
        for child in node.children:
            queue.append(child)


def example_tree() -> Node:
    return Node("A", [Node("B", [Node("D"), Node("E")]), Node("C")])


if __name__ == "__main__":
    for name, root in (
        ("Five-node tree", example_tree()),
        ("Empty tree", None),
        ("Single node", Node("A")),
        ("Wide tree", Node("A", [Node(label) for label in "BCDEF"])),
    ):
        print(f"{name}: ", end="")
        print_bfs(root)
        print()  # The example runner adds a newline; print_bfs does not.
