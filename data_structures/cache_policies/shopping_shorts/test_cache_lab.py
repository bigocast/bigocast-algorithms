"""BigOCast | Moein: exact examples and independent request-history oracle."""

from collections import Counter
from copy import deepcopy
import random
import unittest

from cache_lab import Cache, HISTORY, PRODUCTS, run_example, trace


class ShoppingCacheTests(unittest.TestCase):
    def test_caching_is_two_source_reads_for_three_requests(self):
        rows = run_example("caching")
        self.assertEqual([r["hit"] for r in rows], [False, True, False])
        self.assertEqual([r["reads"] for r in rows], [1, 1, 2])

    def test_lru_and_fifo_react_differently_to_the_same_hit(self):
        lru, fifo = run_example("lru"), run_example("fifo")
        self.assertEqual(lru[3]["recency"], ["P202", "P303", "P101"])
        self.assertEqual(list(fifo[3]["records"]), ["P101", "P202", "P303"])
        self.assertEqual(lru[-1]["evicted"], "P202")
        self.assertEqual(fifo[-1]["evicted"], "P101")
        for rows in (lru, fifo):
            self.assertEqual(rows[-1]["hits"], 1)
            self.assertEqual(rows[-1]["reads"], 4)

    def test_lfu_counts_initial_opening_and_each_hit(self):
        rows = run_example("lfu")
        self.assertEqual({k: e["count"] for k, e in rows[5]["records"].items()},
                         {"P101": 3, "P202": 1, "P303": 2})
        self.assertEqual(rows[-1]["evicted"], "P202")
        self.assertEqual(rows[-1]["records"]["P404"]["count"], 1)

    def test_comparison_restarts_from_identical_history(self):
        runs = run_example("comparison")
        self.assertEqual({p: r[-1]["evicted"] for p, r in runs.items()},
                         {"fifo": "P101", "lru": "P202", "lfu": "P202"})
        for rows in runs.values():
            self.assertEqual(tuple(r["key"] for r in rows[:-1]), HISTORY)
            self.assertEqual(rows[-2]["reads"], 3)
            self.assertEqual(rows[-1]["reads"], 4)
            self.assertEqual(rows[-2]["recency"], ["P202", "P101", "P303"])

    def test_thrashing_and_the_fourth_slot_question(self):
        rows = run_example("thrashing")
        self.assertEqual([r["evicted"] for r in rows],
                         [None, None, None, "P101", "P202", "P303", "P404", "P101"])
        self.assertTrue(all(not r["hit"] for r in rows))
        self.assertEqual(rows[-1]["reads"], 8)
        with_room = trace("lru", tuple(PRODUCTS) * 2, capacity=4)
        self.assertEqual([r["hit"] for r in with_room], [False] * 4 + [True] * 4)
        self.assertEqual(with_room[-1]["reads"], 4)

    def test_freshness_requires_removing_the_stale_copy(self):
        rows = run_example("freshness")
        self.assertEqual(rows[0]["displayed_price"], 300)
        self.assertEqual(rows[2], {"action": "visit", "hit": True, "reads": 1,
                                  "database_price": 250, "saved_price": 300,
                                  "displayed_price": 300})
        self.assertIsNone(rows[3]["saved_price"])
        self.assertFalse(rows[-1]["hit"])
        self.assertEqual(rows[-1]["displayed_price"], 250)
        self.assertEqual(rows[-1]["reads"], 2)

    def test_lfu_ties_use_recency_and_reentry_resets_count(self):
        # Both residents reach two uses; Sony was used less recently.
        rows = trace("lfu", ("P101", "P202", "P101", "P202", "P303", "P101"), 2)
        self.assertEqual(rows[4]["evicted"], "P101")
        self.assertEqual(rows[5]["evicted"], "P303")
        self.assertEqual(rows[5]["records"]["P101"]["count"], 1)

    def test_source_and_returned_snapshots_do_not_mutate_saved_records(self):
        source = deepcopy(PRODUCTS)
        cache = Cache()
        first = cache.request("P101", source)
        source["P101"]["product"] = "changed source"
        first["records"]["P101"]["value"]["product"] = "changed snapshot"
        second = cache.request("P101", source)
        self.assertEqual(second["value"]["product"], "Sony")
        self.assertEqual(second["reads"], 1)
        del source["P101"]
        self.assertTrue(cache.request("P101", source)["hit"])

    def test_invalid_inputs_and_missing_source_leave_state_unchanged(self):
        for capacity in (0, -1, True, 1.5):
            with self.assertRaises(ValueError):
                Cache(capacity=capacity)
        with self.assertRaises(ValueError):
            Cache(policy="unknown")
        cache = Cache(capacity=1)
        cache.request("P101", PRODUCTS)
        before = deepcopy(vars(cache))
        with self.assertRaises(KeyError):
            cache.request("missing", PRODUCTS)
        self.assertEqual(vars(cache), before)

    def test_random_traces_against_independent_request_history(self):
        # This oracle keeps per-resident histories, not simulator timestamps/counts.
        random_source = random.Random(42)
        requests = [random_source.choice(tuple(PRODUCTS)) for _ in range(300)]
        for policy in ("fifo", "lru", "lfu"):
            for capacity in (1, 2, 3, 4):
                with self.subTest(policy=policy, capacity=capacity):
                    residents = []
                    uses = {}
                    hit_flags = []
                    rows = trace(policy, requests, capacity)
                    for step, (key, row) in enumerate(zip(requests, rows)):
                        hit = key in residents
                        victim = None
                        if not hit:
                            if len(residents) == capacity:
                                if policy == "fifo":
                                    victim = residents[0]
                                elif policy == "lru":
                                    victim = min(residents, key=lambda k: uses[k][-1])
                                else:
                                    least_count = min(len(uses[k]) for k in residents)
                                    candidates = [k for k in residents if len(uses[k]) == least_count]
                                    victim = min(candidates, key=lambda k: uses[k][-1])
                                residents.remove(victim)
                                del uses[victim]
                            residents.append(key)
                            uses[key] = []
                        uses[key].append(step)
                        hit_flags.append(hit)
                        self.assertEqual((row["hit"], row["evicted"]), (hit, victim))
                        self.assertEqual(set(row["records"]), set(residents))
                        self.assertEqual(row["recency"], sorted(residents, key=lambda k: uses[k][-1]))
                        self.assertEqual({k: e["count"] for k, e in row["records"].items()},
                                         {k: len(v) for k, v in uses.items()})
                        self.assertEqual(row["reads"], Counter(hit_flags)[False])


if __name__ == "__main__":
    unittest.main()
