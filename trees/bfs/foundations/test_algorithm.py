"""BigOCast | Moein: independent traversal and queue checks for BFS."""

import json
import random
import unittest
from collections import deque
from unittest.mock import patch

import bfs as algorithm
from bfs import (
    Node,
    bfs,
    levels_short_tree,
    main_tree,
    parity_cases,
    queue_short_tree,
    verify,
)


def level_buckets(root):
    """Depth-first collection by depth, independent of a FIFO waiting queue."""
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


def by_depth(root):
    return [node.label for level in level_buckets(root) for node in level]


class BfsTests(unittest.TestCase):
    def check_example(self, build, expected):
        root = build()
        self.assertEqual(bfs(root), expected)
        self.assertEqual(by_depth(root), expected)

    def test_main_example(self):
        self.check_example(main_tree, ["A", "B", "C", "D", "E", "F", "G"])

    def test_levels_short_example(self):
        self.check_example(levels_short_tree, ["R", "Z", "B", "M", "C"])

    def test_queue_short_example(self):
        self.check_example(queue_short_tree, ["A", "B", "C", "D", "E"])

    def test_empty_single_and_independent_default_children(self):
        self.assertEqual(bfs(None), [])
        first, second = Node("first"), Node("second")
        self.assertIsNot(first.children, second.children)
        first.children.append(Node("child"))
        self.assertEqual(second.children, [])
        self.assertEqual(bfs(second), ["second"])

    def test_uneven_tree_keeps_deeper_nodes_behind_the_current_level(self):
        root = Node(
            "R",
            [
                Node("Z", [Node("M", [Node("deep")]), Node("N")]),
                Node("B"),
                Node("A", [Node("C")]),
            ],
        )
        self.assertEqual(bfs(root), ["R", "Z", "B", "A", "M", "N", "C", "deep"])
        self.assertEqual(bfs(root), by_depth(root))

    def test_repeated_labels_are_distinct_nodes_and_input_is_preserved(self):
        left = Node("same", [Node("leaf")])
        right = Node("same", [Node("leaf")])
        root = Node("same", [left, right])
        nodes = [node for level in level_buckets(root) for node in level]
        before = [(node.label, tuple(map(id, node.children))) for node in nodes]
        self.assertIsNot(left, right)
        self.assertNotEqual(left, right)
        first = bfs(root)
        self.assertEqual(first, ["same", "same", "same", "leaf", "leaf"])
        first.append("only in the result")
        self.assertEqual(bfs(root), ["same", "same", "same", "leaf", "leaf"])
        self.assertEqual(bfs(root), by_depth(root))
        self.assertEqual(before, [(node.label, tuple(map(id, node.children))) for node in nodes])

    def test_chain_has_no_recursion_limit(self):
        root = tail = Node("0")
        for number in range(1, 5000):
            child = Node(str(number))
            tail.children.append(child)
            tail = child
        self.assertEqual(bfs(root), [str(number) for number in range(5000)])

    def test_wide_tree_does_not_drop_waiting_children(self):
        labels = [str(number) for number in range(4096, 0, -1)]
        root = Node("root", [Node(label) for label in labels])
        self.assertEqual(bfs(root), ["root", *labels])

    def check_queue(self, build, width, peak):
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

        root = build()
        expected = by_depth(root)
        with patch.object(algorithm, "deque", ObservedDeque):
            self.assertEqual(bfs(root), expected)
        self.assertEqual(len(queues), 1)
        waiting = queues[0]
        self.assertIsNone(waiting.maxlen)
        self.assertFalse(waiting)
        self.assertEqual(max(map(len, waiting.states)), peak)
        self.assertEqual(max(map(len, level_buckets(root))), width)
        self.assertEqual([node.label for node in waiting.removed], expected)
        self.assertEqual(len(waiting.inserted), len(expected))
        self.assertEqual(len(waiting.removed), len(expected))
        self.assertEqual(len(set(map(id, waiting.inserted))), len(expected))
        return [[node.label for node in state] for state in waiting.states]

    def test_main_queue_peak_and_insertions(self):
        self.check_queue(main_tree, 4, 4)

    def test_levels_short_queue_peak_and_insertions(self):
        self.check_queue(levels_short_tree, 2, 2)

    def test_queue_short_peak_exceeds_level_width(self):
        states = self.check_queue(queue_short_tree, 2, 3)
        self.assertIn(["C", "D", "E"], states)

    def test_generated_small_ordered_trees_against_depth_buckets(self):
        rng = random.Random(20260925)
        checked = 0
        for size in range(65):
            for trial in range(8):
                with self.subTest(size=size, trial=trial):
                    nodes = [Node(f"label-{number}") for number in range(size)]
                    for index in range(1, size):
                        parent = nodes[rng.randrange(index)]
                        parent.children.insert(
                            rng.randrange(len(parent.children) + 1), nodes[index]
                        )
                    root = nodes[0] if nodes else None
                    actual = bfs(root)
                    self.assertEqual(actual, by_depth(root))
                    self.assertEqual(len(actual), size)
                    checked += 1
        self.assertEqual(checked, 520)

    def test_parity_fixtures_and_lesson_verification(self):
        def from_data(value):
            if value is None:
                return None
            return Node(value["label"], [from_data(child) for child in value["children"]])

        cases = parity_cases()
        self.assertEqual(len(cases), 8)
        for case in cases:
            root = from_data(json.loads(case["input"]["tree"]))
            self.assertEqual(case["expected"], {"order": by_depth(root)})
            self.assertEqual(bfs(root), case["expected"]["order"])
        report = verify()
        self.assertEqual(report["checked"], len(cases))
        self.assertEqual(report["example"], ["A", "B", "C", "D", "E", "F", "G"])
        self.assertEqual(report["short_levels"], ["R", "Z", "B", "M", "C"])
        self.assertEqual(report["short_queue"], ["A", "B", "C", "D", "E"])
        self.assertEqual(report["empty"], [])
        json.dumps(report)


if __name__ == "__main__":
    unittest.main()
