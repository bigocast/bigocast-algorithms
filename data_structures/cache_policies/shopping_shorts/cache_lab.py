"""BigOCast | Moein: seven independent shopping-cache examples.

Python 3.10+, standard library only. This is an inspectable policy simulator,
not an O(1) cache implementation. See README.md for contracts and costs.
"""

import argparse
from copy import deepcopy
from dataclasses import dataclass
import json


PRODUCTS = {
    "P101": {"product": "Sony"},
    "P202": {"product": "Bose"},
    "P303": {"product": "AirPods"},
    "P404": {"product": "Momentum"},
}
HISTORY = ("P101", "P202", "P303", "P101", "P101", "P303")
EXAMPLES = ("caching", "lru", "fifo", "lfu", "comparison", "thrashing", "freshness")


@dataclass
class Entry:
    value: object
    arrival: int
    last: int
    count: int = 1


class Cache:
    """A bounded FIFO/LRU/LFU cache with source reads on misses.

    LFU counts the initial fetch as one use and resets the count on re-entry.
    Equal LFU counts are resolved by least recent use. A hit never rereads the
    source or refreshes the saved value. Source values are copied on admission.
    """

    def __init__(self, policy="lru", capacity=3):
        if policy not in ("fifo", "lru", "lfu"):
            raise ValueError("policy must be fifo, lru or lfu")
        if type(capacity) is not int or capacity < 1:
            raise ValueError("capacity must be a positive integer")
        self.policy = policy
        self.capacity = capacity
        self.records = {}
        self.tick = 0
        self.reads = 0
        self.hits = 0

    def request(self, key, source):
        hit = key in self.records
        # Resolve the source first so an unknown product leaves state unchanged.
        if not hit:
            value = deepcopy(source[key])
        self.tick += 1
        evicted = None
        if hit:
            entry = self.records[key]
            entry.last = self.tick
            entry.count += 1
            self.hits += 1
        else:
            if len(self.records) == self.capacity:
                if self.policy == "fifo":
                    rank = lambda k: self.records[k].arrival
                elif self.policy == "lru":
                    rank = lambda k: self.records[k].last
                else:
                    rank = lambda k: (self.records[k].count, self.records[k].last)
                evicted = min(self.records, key=rank)
                del self.records[evicted]
            self.reads += 1
            self.records[key] = Entry(value, self.tick, self.tick)
        return {
            "key": key,
            "hit": hit,
            "evicted": evicted,
            "reads": self.reads,
            "hits": self.hits,
            "value": deepcopy(self.records[key].value),
            "records": {
                k: {"value": deepcopy(e.value), "arrival": e.arrival,
                    "last": e.last, "count": e.count}
                for k, e in self.records.items()
            },
            "recency": sorted(self.records, key=lambda k: self.records[k].last),
        }


def trace(policy, requests, capacity=3):
    """Return independent snapshots after each request to the sample source."""
    cache = Cache(policy, capacity)
    return [cache.request(key, PRODUCTS) for key in requests]


def freshness_example():
    """A plain saved-copy dictionary; no eviction policy is involved."""
    source = {"P101": {"product": "Sony", "price": 300}}
    saved = {}
    reads = 0
    steps = []

    def visit():
        nonlocal reads
        hit = "P101" in saved
        if not hit:
            reads += 1
            saved["P101"] = deepcopy(source["P101"])
        result = {"action": "visit", "hit": hit, "reads": reads,
                  "database_price": source["P101"]["price"],
                  "saved_price": saved["P101"]["price"],
                  "displayed_price": saved["P101"]["price"]}
        steps.append(result)
        return result

    visit()
    source["P101"]["price"] = 250
    steps.append({"action": "source changes", "database_price": 250,
                  "saved_price": 300, "reads": reads})
    visit()  # A hit finds a copy, but does not prove that copy is current.
    del saved["P101"]
    steps.append({"action": "invalidate", "database_price": 250,
                  "saved_price": None, "reads": reads})
    visit()
    return steps


def run_example(name):
    """Run one Short's complete example, without running another first."""
    if name == "caching":
        return trace("lru", ("P101", "P101", "P202"))
    if name in ("lru", "fifo"):
        return trace(name, ("P101", "P202", "P303", "P101", "P404"))
    if name == "lfu":
        return trace("lfu", HISTORY + ("P404",))
    if name == "comparison":
        # Each policy receives a fresh cache and the identical full history.
        return {policy: trace(policy, HISTORY + ("P404",))
                for policy in ("fifo", "lru", "lfu")}
    if name == "thrashing":
        return trace("lru", tuple(PRODUCTS) * 2)
    if name == "freshness":
        return freshness_example()
    raise ValueError(f"unknown example: {name}")


def summarize(name, result):
    if name == "comparison":
        choices = "; ".join(f"{policy.upper()} removes {PRODUCTS[rows[-1]['evicted']]['product']}"
                            for policy, rows in result.items())
        return f"comparison: {choices}"
    if name == "freshness":
        return (f"freshness: first ${result[0]['displayed_price']}; "
                f"stale hit ${result[2]['displayed_price']}; "
                f"after invalidation ${result[-1]['displayed_price']}; "
                f"{result[-1]['reads']} database reads")
    end = result[-1]
    hit_word = "hit" if end["hits"] == 1 else "hits"
    summary = (f"{name}: {len(result)} requests, {end['hits']} {hit_word}, "
               f"{end['reads']} database reads")
    if end["evicted"]:
        summary += f"; last removed {PRODUCTS[end['evicted']]['product']}"
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("example", nargs="?", choices=("all",) + EXAMPLES, default="all")
    parser.add_argument("--trace", action="store_true", help="also print every state as JSON")
    args = parser.parse_args()
    for name in EXAMPLES if args.example == "all" else (args.example,):
        result = run_example(name)
        print(summarize(name, result))
        if args.trace:
            print(json.dumps(result, indent=2))
