"""BigOCast | Moein. LRU cache with a dictionary and doubly linked list.

Run this file to reproduce the lesson and six Shorts. Standard library only.
Capacity counts entries. Keys must be hashable; values may be any Python object.
get raises KeyError on a miss. The caller, not the cache, fetches missing data.

get/put take expected, amortized O(1) time with constant-cost, stable hashing and
equality. Pathological collisions can make dictionary work linear in capacity.
Metadata uses O(capacity) space, plus the referenced payloads. Fetching, producing
or copying payloads is outside these cache-operation bounds. This example does
not add synchronization, expiration or invalidation.
"""


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        if (
            isinstance(capacity, bool)
            or not isinstance(capacity, int)
            or capacity < 1
        ):
            raise ValueError("Capacity must be a positive integer.")
        self.capacity = capacity
        self.nodes = {}
        # Endpoints are not entries and do not use capacity.
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _append(self, node):
        newest = self.tail.prev
        newest.next = node
        node.prev = newest
        node.next = self.tail
        self.tail.prev = node

    def get(self, key):
        node = self.nodes[key]
        self._unlink(node)
        self._append(node)
        return node.value

    def put(self, key, value):
        if key in self.nodes:
            node = self.nodes[key]
            node.value = value
            self._unlink(node)
        else:
            if len(self.nodes) == self.capacity:
                victim = self.head.next
                self._unlink(victim)
                del self.nodes[victim.key]
            node = Node(key, value)
            self.nodes[key] = node
        self._append(node)

    def __len__(self):
        return len(self.nodes)

    def items(self):
        """Diagnostic snapshot, LRU to MRU. This traversal costs O(capacity)."""
        result = []
        node = self.head.next
        while node is not self.tail:
            result.append((node.key, node.value))
            node = node.next
        return result


PICTURES = {10: "cat", 20: "lake", 30: "tree", 40: "boat"}
MAIN_REQUESTS = (10, 20, 30, 10, 40, 10, 20)
CYCLE_REQUESTS = (10, 20, 30, 40, 10, 20, 30, 40)
SHORT_REQUESTS = {
    "caching": (10, 10),
    "hit_miss": (10, 20, 10, 30, 20),
    "eviction": (10, 20, 30, 10, 40),
    "lookup": (10, 20, 30, 20),
    "reorder": (10, 20, 30, 20),
    "all_misses": CYCLE_REQUESTS,
}


def request_trace(requests=MAIN_REQUESTS, capacity=3):
    """Caller loads on misses; snapshots add O(n * capacity) work and storage.

    Snapshot traversal is outside the get/put bounds stated in the module contract.
    """
    cache = LRUCache(capacity)
    steps = []
    hits = misses = 0
    for key in requests:
        if key not in PICTURES:
            raise ValueError("Picture keys are 10, 20, 30 and 40.")
        before = [item[0] for item in cache.items()]
        evicted = None
        try:
            value = cache.get(key)
            hit = True
            hits += 1
        except KeyError:
            hit = False
            misses += 1
            if len(cache) == capacity:
                evicted = before[0]
            value = PICTURES[key]  # Stand-in for fetching the original picture.
            cache.put(key, value)
        order = [item[0] for item in cache.items()]
        steps.append({
            "key": key, "picture": value, "hit": hit, "evicted": evicted,
            "order": order, "pictures": [PICTURES[item] for item in order],
            "hits": hits, "misses": misses,
        })
    return {"capacity": capacity, "hits": hits, "misses": misses, "steps": steps}


def experiment(inputs):
    """The portable experiment's small, explicit input contract."""
    if any(not isinstance(inputs.get(name), str) or len(inputs[name]) > 200
           for name in ("capacity", "requests")):
        raise ValueError("Inputs must be text fields of at most 200 characters.")
    text = inputs["capacity"].strip(" \t\r\n")
    if text not in {"1", "2", "3", "4"}:
        raise ValueError("Choose a capacity from 1 to 4.")
    names = [name.strip(" \t\r\n").lower() for name in inputs["requests"].split(",")]
    keys = {value: key for key, value in PICTURES.items()}
    if not 1 <= len(names) <= 20 or any(name not in keys for name in names):
        raise ValueError("Enter 1 to 20 picture names: cat, lake, tree or boat.")
    return request_trace([keys[name] for name in names], int(text))


def parity_cases():
    cases = [
        {"capacity": "3", "requests": "cat, lake, tree, cat, boat, cat, lake"},
        {"capacity": "3", "requests": "cat,lake,tree,boat,cat,lake,tree,boat"},
        {"capacity": "4", "requests": "cat,lake,tree,boat,cat,lake,tree,boat"},
        {"capacity": "1", "requests": "cat,cat,lake,lake,cat"},
        {"capacity": "2", "requests": "Cat, LAKE, cat, tree, lake"},
        {"capacity": "3", "requests": "tree"},
    ]
    return [{"input": case, "expected": experiment(case)} for case in cases]


def verify():
    main = request_trace()
    assert [step["order"] for step in main["steps"]] == [
        [10], [10, 20], [10, 20, 30], [20, 30, 10],
        [30, 10, 40], [30, 40, 10], [40, 10, 20],
    ]
    assert (main["hits"], main["misses"]) == (2, 5)
    cycle = request_trace(CYCLE_REQUESTS)
    expanded = request_trace(CYCLE_REQUESTS, 4)
    assert (cycle["hits"], cycle["misses"]) == (0, 8)
    assert (expanded["hits"], expanded["misses"]) == (4, 4)
    classification = request_trace(SHORT_REQUESTS["hit_miss"], 3)
    assert (classification["hits"], classification["misses"]) == (2, 3)
    return {"main_hits": 2, "main_misses": 5, "cycle_misses": 8,
            "expanded_hits": 4, "hit_miss_short": [2, 3]}


if __name__ == "__main__":
    print("LRU cache | BigOCast | Moein")
    examples = {"Long lesson": (MAIN_REQUESTS, 3),
                **{name: (values, 2 if name == "caching" else 3)
                   for name, values in SHORT_REQUESTS.items()},
                "Four slots": (CYCLE_REQUESTS, 4)}
    for title, (values, capacity) in examples.items():
        result = request_trace(values, capacity)
        print(f"\n{title} (capacity {capacity})")
        for step in result["steps"]:
            victim = f"; evict {PICTURES[step['evicted']]}" if step["evicted"] else ""
            print(f"  {step['picture']:4s}: {'HIT ' if step['hit'] else 'MISS'}{victim}; "
                  f"LRU → MRU: {', '.join(step['pictures'])}")
        print(f"  {result['hits']} hits, {result['misses']} misses/source fetches")
    print("\nChecks:", verify())
