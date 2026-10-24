"""BigOCast | Moein. Known results and an independent relaxation oracle."""
from copy import deepcopy
from math import inf
import random
import unittest
from dijkstra import GRAPH, shortest_path
from edge_cases import ZERO_CYCLE, NEGATIVE, UNREACHABLE


def bellman_ford_cost(graph, start, goal):
    distances = {node: inf for node in graph}
    distances[start] = 0
    for _ in range(len(graph) - 1):
        changed = False
        for node, roads in graph.items():
            for neighbor, weight in roads:
                candidate = distances[node] + weight
                if candidate < distances[neighbor]:
                    distances[neighbor] = candidate
                    changed = True
        if not changed:
            break
    return distances[goal]


class DijkstraTests(unittest.TestCase):
    def test_delivery_and_input_preservation(self):
        before = deepcopy(GRAPH)
        self.assertEqual(shortest_path(GRAPH, "Depot", "Home"),
                         (7, ["Depot", "Market", "Home"]))
        self.assertEqual(GRAPH, before)

    def test_improved_bridge(self):
        self.assertEqual(shortest_path(GRAPH, "Depot", "Bridge"),
                         (3, ["Depot", "Park", "Bridge"]))

    def test_tied_routes_and_zero_cycle(self):
        self.assertEqual(shortest_path(ZERO_CYCLE, "S", "T"), (2, ["S", "T"]))

    def test_unreachable_and_same_goal(self):
        self.assertEqual(shortest_path(UNREACHABLE, "Depot", "Home"), (inf, []))
        self.assertEqual(shortest_path(GRAPH, "Depot", "Depot"), (0, ["Depot"]))
        self.assertEqual(shortest_path({"S": []}, "S", "S"), (0, ["S"]))

    def test_direction_and_zero_self_loop(self):
        self.assertEqual(shortest_path(GRAPH, "Home", "Depot"), (inf, []))
        self.assertEqual(shortest_path({"S": [("S", 0), ("T", 0)], "T": []}, "S", "T"),
                         (0, ["S", "T"]))

    def test_invalid_contract(self):
        for graph, start, goal in [
            (NEGATIVE, "S", "T"), (NEGATIVE, "S", "S"),
            ({"S": [("T", True)], "T": []}, "S", "T"),
            ({"S": [("T", 1.5)], "T": []}, "S", "T"),
            ({"S": [("missing", 1)]}, "S", "S"),
            ({"S": []}, "missing", "S"),
            ({1: []}, 1, 1),
        ]:
            with self.subTest(graph=graph, start=start, goal=goal):
                with self.assertRaises(ValueError):
                    shortest_path(graph, start, goal)

    def test_against_independent_oracle(self):
        rng = random.Random(20261024)
        for size in range(1, 8):
            nodes = [str(i) for i in range(size)]
            for _ in range(25):
                graph = {a: [(b, rng.randrange(6)) for b in nodes if rng.random() < .3]
                         for a in nodes}
                for start in nodes:
                    for goal in nodes:
                        cost, path = shortest_path(graph, start, goal)
                        self.assertEqual(cost, bellman_ford_cost(graph, start, goal))
                        if cost == inf:
                            self.assertEqual(path, [])
                            continue
                        self.assertEqual((path[0], path[-1]), (start, goal))
                        self.assertEqual(len(path), len(set(path)))
                        self.assertEqual(sum(dict(graph[a])[b] for a, b in zip(path, path[1:])), cost)


if __name__ == "__main__":
    unittest.main()
