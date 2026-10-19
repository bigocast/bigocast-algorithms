"""BigOCast | Moein. Correctness and bidirectional-link checks for the taught cache."""

import random
import unittest
from collections import OrderedDict

from api_cache import CYCLE_REQUESTS, LRUCache, experiment, request_trace, verify


class CacheTests(unittest.TestCase):
    def assert_links(self, cache, expected):
        self.assertEqual(len(cache), len(expected))
        self.assertLessEqual(len(cache), cache.capacity)
        self.assertIsNone(cache.head.prev)
        self.assertIsNone(cache.tail.next)
        seen = []
        previous = cache.head
        node = previous.next
        while node is not cache.tail:
            self.assertLess(len(seen), len(expected))
            self.assertNotIn(id(node), seen)
            seen.append(id(node))
            self.assertIs(node.prev, previous)
            self.assertIs(cache.nodes[node.key], node)
            previous, node = node, node.next
        self.assertIs(cache.tail.prev, previous)
        reverse = []
        following = cache.tail
        node = following.prev
        while node is not cache.head:
            self.assertLess(len(reverse), len(expected))
            self.assertIs(node.next, following)
            reverse.append(node.key)
            following, node = node, node.prev
        self.assertIs(cache.head.next, following)
        self.assertEqual(reverse, list(reversed(expected)))
        self.assertEqual(cache.items(), list(expected.items()))

    def test_lesson_and_counterexample(self):
        self.assertEqual(verify()["main_hits"], 3)
        self.assertEqual(request_trace(CYCLE_REQUESTS)["misses"], 8)
        self.assertEqual(request_trace(CYCLE_REQUESTS, 4)["hits"], 4)

    def test_middle_access_preserves_node_identity(self):
        cache = LRUCache(3)
        for key in (10, 20, 30):
            cache.put(key, str(key))
        original = cache.nodes[20]
        self.assertEqual(cache.get(20), "20")
        self.assertIs(cache.nodes[20], original)
        self.assert_links(cache, OrderedDict([(10, "10"), (30, "30"), (20, "20")]))

    def test_update_promotes_without_consuming_a_slot(self):
        cache = LRUCache(2)
        cache.put(10, "42")
        cache.put(20, "lake")
        node = cache.nodes[10]
        cache.put(10, "new cat")
        self.assertIs(cache.nodes[10], node)
        self.assert_links(cache, OrderedDict([(20, "lake"), (10, "new cat")]))
        cache.put(30, "tree")
        self.assert_links(cache, OrderedDict([(10, "new cat"), (30, "tree")]))
        with self.assertRaises(KeyError):
            cache.get(20)

    def test_missing_get_does_not_mutate(self):
        cache = LRUCache(2)
        cache.put(10, None)
        cache.put(20, "lake")
        with self.assertRaises(KeyError):
            cache.get(99)
        self.assert_links(cache, OrderedDict([(10, None), (20, "lake")]))
        self.assertIsNone(cache.get(10))
        self.assert_links(cache, OrderedDict([(20, "lake"), (10, None)]))

    def test_one_slot_empty_and_none_key(self):
        cache = LRUCache(1)
        self.assert_links(cache, OrderedDict())
        cache.put(None, "first")
        self.assertEqual(cache.get(None), "first")
        cache.put(None, "updated")
        self.assert_links(cache, OrderedDict([(None, "updated")]))
        cache.put("new", "next")
        self.assert_links(cache, OrderedDict([("new", "next")]))
        with self.assertRaises(KeyError):
            cache.get(None)

    def test_capacities_and_hashability(self):
        for capacity in (0, -1, True, 1.5, "3", None):
            with self.subTest(capacity=capacity), self.assertRaises(ValueError):
                LRUCache(capacity)
        cache = LRUCache(2)
        with self.assertRaises(TypeError):
            cache.put([], "unhashable")
        self.assertEqual(cache.items(), [])

    def test_mixed_operations_match_independent_ordered_dict(self):
        randomizer = random.Random(146)
        for capacity in (1, 2, 3, 7):
            cache = LRUCache(capacity)
            oracle = OrderedDict()
            for _ in range(500):
                key = randomizer.randrange(10)
                if randomizer.random() < 0.55:
                    value = randomizer.randrange(100)
                    cache.put(key, value)
                    oracle[key] = value
                    oracle.move_to_end(key)
                    if len(oracle) > capacity:
                        oracle.popitem(last=False)
                elif key in oracle:
                    self.assertEqual(cache.get(key), oracle[key])
                    oracle.move_to_end(key)
                else:
                    with self.assertRaises(KeyError):
                        cache.get(key)
                self.assert_links(cache, oracle)

    def test_experiment_contract(self):
        self.assertEqual(experiment({"capacity": " 3 ", "requests": "42, 42"})["hits"], 1)
        invalid = [
            {"capacity": "0", "requests": "42"},
            {"capacity": "3.0", "requests": "42"},
            {"capacity": "3", "requests": ""},
            {"capacity": "3", "requests": "42,"},
            {"capacity": "3", "requests": "99"},
            {"capacity": "3", "requests": ",".join(["42"] * 21)},
            {"capacity": "3", "requests": "x" * 201},
            {"capacity": 3, "requests": "42"},
        ]
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ValueError):
                experiment(value)


if __name__ == "__main__":
    unittest.main()
