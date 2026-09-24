"""BigOCast | Moein: independent breadth-first oracle for the 8-puzzle example."""

import unittest
from collections import deque
from itertools import permutations

import a_star as a


def oracle_neighbors(board):
    """Find adjacent slots directly, without calling the A* successor helper."""
    empty = board.index(0)
    for other in range(9):
        if abs(empty // 3 - other // 3) + abs(empty % 3 - other % 3) == 1:
            result = list(board)
            result[empty], result[other] = result[other], result[empty]
            yield tuple(result)


class PuzzleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.distance = {a.GOAL: 0}
        queue = deque([a.GOAL])
        while queue:
            board = queue.popleft()
            for nxt in oracle_neighbors(board):
                if nxt not in cls.distance:
                    cls.distance[nxt] = cls.distance[board] + 1
                    queue.append(nxt)

    def test_finite_state_space(self):
        self.assertEqual(len(self.distance), 181440)
        self.assertEqual(max(self.distance.values()), 31)

    def test_exact_four_move_example(self):
        self.assertEqual(a.manhattan(a.START), 4)
        self.assertEqual(a.a_star(a.START), [
            a.START,
            (1, 2, 3, 0, 5, 6, 4, 7, 8),
            (1, 2, 3, 4, 5, 6, 0, 7, 8),
            (1, 2, 3, 4, 5, 6, 7, 0, 8),
            a.GOAL,
        ])

    def test_exact_three_move_estimate_example(self):
        self.assertEqual(a.manhattan(a.ESTIMATE_EXAMPLE), 3)
        self.assertEqual(a.a_star(a.ESTIMATE_EXAMPLE), [
            a.ESTIMATE_EXAMPLE,
            (1, 2, 3, 4, 0, 5, 7, 8, 6),
            (1, 2, 3, 4, 5, 0, 7, 8, 6),
            a.GOAL,
        ])

    def test_one_shortest_solution_at_every_depth(self):
        examples = {}
        for board, depth in self.distance.items():
            examples.setdefault(depth, board)
        for depth, board in examples.items():
            with self.subTest(depth=depth):
                path = a.a_star(board)
                self.assertEqual((path[0], path[-1], len(path) - 1), (board, a.GOAL, depth))
                self.assertTrue(all(
                    right in tuple(oracle_neighbors(left))
                    for left, right in zip(path, path[1:])
                ))

    def test_heuristic_and_successors_against_all_reachable_states(self):
        for board, distance in self.distance.items():
            h = a.manhattan(board)
            self.assertLessEqual(h, distance)
            self.assertEqual(set(a.neighbors(board)), set(oracle_neighbors(board)))
            self.assertTrue(all(
                abs(h - a.manhattan(nxt)) == 1 for nxt in oracle_neighbors(board)
            ))

    def test_parity_matches_reachability_for_every_permutation(self):
        for board in permutations(range(9)):
            self.assertEqual(a.solvable(board), board in self.distance)

    def test_impossible_and_already_solved(self):
        self.assertIsNone(a.a_star((1, 2, 3, 4, 5, 6, 8, 7, 0)))
        self.assertEqual(a.a_star(a.GOAL), [a.GOAL])

    def test_input_is_not_mutated(self):
        original = list(a.START)
        a.a_star(original)
        self.assertEqual(original, list(a.START))

    def test_invalid_boards(self):
        for board in (
            [], [0] * 9, list(range(1, 10)),
            [True, 0, 2, 3, 4, 5, 6, 7, 8], [0.0, 1, 2, 3, 4, 5, 6, 7, 8],
        ):
            with self.subTest(board=board), self.assertRaises(ValueError):
                a.a_star(board)

    def test_text_input_contract(self):
        self.assertEqual(a.parse_input("1 2 3 / 5 0 6 / 4 7 8"), a.START)
        self.assertEqual(a.parse_input("1,2,3,4,5,6,7,8,0"), a.GOAL)
        for text in (
            "", "1 2 3", "1 2 3 4 5 6 7 8 9", "1 1 2 3 4 5 6 7 8",
            "１ 2 3 4 5 6 7 8 0", "1\n2 3 4 5 6 7 8 0", " " * 101, None,
        ):
            with self.subTest(text=text), self.assertRaises(ValueError):
                a.parse_input(text)


if __name__ == "__main__":
    unittest.main()
