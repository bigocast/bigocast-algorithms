"""BigOCast | Moein: stdout, ordering and queue checks for printing BFS."""

import random
import unittest
from collections import deque
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import print_bfs as algorithm
from print_bfs import Node, example_tree, print_bfs


def capture(root):
    stream = StringIO()
    with redirect_stdout(stream):
        result = print_bfs(root)
    return result, stream.getvalue()


def level_buckets(root):
    """Collect by depth using a stack, independently of a FIFO queue."""
    if root is None:
        return []
    levels = []
    stack = [(root, 0)]
    while stack:
        node, depth = stack.pop()
        if depth == len(levels):
            levels.append([])
        levels[depth].append(node)
        stack.extend((child, depth + 1) for child in reversed(node.children))
    return levels


class PrintBfsTests(unittest.TestCase):
    def test_five_node_example_has_trailing_space_and_no_newline(self):
        self.assertEqual(capture(example_tree()), (None, "A B C D E "))

    def test_empty_tree_returns_silently(self):
        self.assertEqual(capture(None), (None, ""))

    def test_single_node_and_independent_default_children(self):
        first, second = Node("A"), Node("B")
        self.assertIsNot(first.children, second.children)
        first.children.append(Node("child"))
        self.assertEqual(second.children, [])
        self.assertEqual(capture(second), (None, "B "))

    def test_children_keep_their_order_without_sorting_labels(self):
        root = Node("R", [Node("Z"), Node("B"), Node("M"), Node("C")])
        self.assertEqual(capture(root), (None, "R Z B M C "))

    def test_uneven_tree_finishes_earlier_levels_first(self):
        root = Node(
            "R",
            [Node("Z", [Node("M", [Node("deep")]), Node("N")]), Node("B")],
        )
        self.assertEqual(capture(root), (None, "R Z B M N deep "))

    def test_repeated_labels_are_printed_and_input_is_unchanged(self):
        root = Node("same", [Node("same"), Node("same", [Node("leaf")])])
        nodes = [node for level in level_buckets(root) for node in level]
        before = [(node.label, tuple(map(id, node.children))) for node in nodes]
        self.assertEqual(capture(root), (None, "same same same leaf "))
        self.assertEqual(capture(root), (None, "same same same leaf "))
        self.assertEqual(
            before, [(node.label, tuple(map(id, node.children))) for node in nodes]
        )

    def test_long_chain_does_not_require_recursion(self):
        root = tail = Node("0")
        for number in range(1, 3000):
            child = Node(str(number))
            tail.children.append(child)
            tail = child
        self.assertEqual(capture(root), (None, "".join(f"{n} " for n in range(3000))))

    def test_wide_tree_does_not_drop_waiting_children(self):
        labels = [str(number) for number in range(4096, 0, -1)]
        root = Node("root", [Node(label) for label in labels])
        self.assertEqual(
            capture(root), (None, "root " + "".join(f"{x} " for x in labels))
        )

    def test_actual_queue_is_unbounded_and_straddles_two_levels(self):
        queues = []

        class ObservedDeque(deque):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.states = [list(self)]
                self.inserted = list(self)
                self.removed = []
                queues.append(self)

            def append(self, child):
                super().append(child)
                self.inserted.append(child)
                self.states.append(list(self))

            def popleft(self):
                node = super().popleft()
                self.removed.append(node)
                self.states.append(list(self))
                return node

        root = example_tree()
        with patch.object(algorithm, "deque", ObservedDeque):
            self.assertEqual(capture(root), (None, "A B C D E "))
        self.assertEqual(len(queues), 1)
        waiting = queues[0]
        self.assertIsNone(waiting.maxlen)
        self.assertFalse(waiting)
        self.assertEqual(max(map(len, level_buckets(root))), 2)
        self.assertEqual(max(map(len, waiting.states)), 3)
        self.assertIn(
            ["C", "D", "E"], [[n.label for n in row] for row in waiting.states]
        )
        self.assertEqual([node.label for node in waiting.removed], list("ABCDE"))
        self.assertEqual(len(waiting.inserted), 5)
        self.assertEqual(len(set(map(id, waiting.inserted))), 5)

    def test_generated_trees_against_independent_depth_buckets(self):
        rng = random.Random(20260925)
        for size in range(65):
            for trial in range(8):
                with self.subTest(size=size, trial=trial):
                    nodes = [
                        Node(rng.choice(("Z", "A", "M", "C"))) for _ in range(size)
                    ]
                    for index in range(1, size):
                        parent = nodes[rng.randrange(index)]
                        parent.children.insert(
                            rng.randrange(len(parent.children) + 1), nodes[index]
                        )
                    root = nodes[0] if nodes else None
                    expected = "".join(
                        f"{node.label} "
                        for level in level_buckets(root)
                        for node in level
                    )
                    self.assertEqual(capture(root), (None, expected))


if __name__ == "__main__":
    unittest.main()
