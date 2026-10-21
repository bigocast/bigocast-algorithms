"""BigOCast | Moein: a capacity-bounded LRU cache and the shopping example.

get returns None on a miss. Product records are dictionaries, so None is unambiguous.
put inserts or updates and counts as a use. Capacity zero retains nothing.
The dictionary stores references to the same nodes used by the linked list.
This single-threaded teaching implementation does not implement freshness.
"""

from dataclasses import dataclass


@dataclass(eq=False)
class Node:
    key: str | None = None
    value: object = None
    prev: "Node | None" = None
    next: "Node | None" = None


class LRUCache:
    def __init__(self, capacity: int):
        if (
            isinstance(capacity, bool)
            or not isinstance(capacity, int)
            or capacity < 0
        ):
            raise ValueError("invalid cache capacity")
        self.capacity = capacity
        self.nodes: dict[str, Node] = {}
        self.left, self.right = Node(), Node()
        self.left.next = self.right
        self.right.prev = self.left

    def _remove(self, node: Node) -> None:
        before, after = node.prev, node.next
        before.next = after
        after.prev = before

    def _append(self, node: Node) -> None:
        last = self.right.prev
        last.next = node
        node.prev = last
        node.next = self.right
        self.right.prev = node

    def get(self, key: str):
        node = self.nodes.get(key)
        if node is None:
            return None
        self._remove(node)
        self._append(node)
        return node.value

    def put(self, key: str, value: dict) -> None:
        if not isinstance(value, dict):
            raise TypeError("record must be a dictionary")
        if self.capacity == 0:
            return
        if key in self.nodes:
            node = self.nodes[key]
            node.value = value
            self._remove(node)
            self._append(node)
            return
        if len(self.nodes) == self.capacity:
            oldest = self.left.next
            self._remove(oldest)
            del self.nodes[oldest.key]
        node = Node(key, value)
        self.nodes[key] = node
        self._append(node)

    def order(self) -> list[str]:
        """Inspection only, O(C); never called by get or put."""
        result, current = [], self.left.next
        while current is not self.right:
            result.append(current.key)
            current = current.next
        return result

    def check(self) -> None:
        """Check every forward/backward link and dictionary reference for tests."""
        current, keys = self.left, []
        while current.next is not None:
            following = current.next
            assert following.prev is current
            if following is not self.right:
                assert self.nodes[following.key] is following
                keys.append(following.key)
                assert len(keys) <= self.capacity
            current = following
        assert current is self.right and set(keys) == set(self.nodes)
        assert len(keys) == len(self.nodes)


PRODUCTS = {
    "P101": {"brand": "Sony", "model": "WH-1000XM5", "category": "Over-ear headphones"},
    "P202": {"brand": "Bose", "model": "QuietComfort", "category": "Over-ear headphones"},
    "P303": {"brand": "Apple", "model": "AirPods Max", "category": "Over-ear headphones"},
    "P404": {
        "brand": "Sennheiser",
        "model": "MOMENTUM 4 Wireless",
        "category": "Over-ear headphones",
    },
}
REQUESTS = ("P101", "P202", "P101", "P303", "P101", "P202", "P404", "P101")


def run_requests(requests=REQUESTS, capacity=3):
    cache, reads, result = LRUCache(capacity), 0, []
    for key in requests:
        before = cache.order()
        value = cache.get(key)
        hit = value is not None
        if not hit:
            reads += 1
            value = PRODUCTS[key].copy()
            cache.put(key, value)
            hit = False
        cache.check()
        after = cache.order()
        result.append(
            {
                "key": key,
                "hit": hit,
                "before": before,
                "after": after,
                "reads": reads,
                "evicted": next((k for k in before if k not in after), None),
            }
        )
    return result


def implementation_walkthrough():
    """The exact dictionary/list examples shown beside the Python code."""
    cache = LRUCache(3)
    for key in ("P202", "P404", "P101"):
        cache.put(key, PRODUCTS[key].copy())
    states = {"request_trace_end": cache.order()}
    momentum = cache.nodes["P404"]
    cache.get("P404")
    assert cache.nodes["P404"] is momentum
    states["structures_end"] = cache.order()
    sony = cache.nodes["P101"]
    cache._remove(sony)
    cache._append(sony)
    cache.check()
    states["helpers_end"] = cache.order()
    cache.get("P404")
    states["get_end"] = cache.order()
    assert cache.get("P303") is None
    bose = cache.nodes["P202"]
    cache.put("P202", {**PRODUCTS["P202"], "category": "Wireless"})
    assert cache.nodes["P202"] is bose
    states["update_end"] = cache.order()
    cache.put("P303", PRODUCTS["P303"].copy())
    cache.check()
    states["insert_end"] = cache.order()
    assert "P101" not in cache.nodes
    return states


def verify():
    """Independent OrderedDict oracle plus update identity and boundary checks."""
    from collections import OrderedDict
    from random import Random

    expected = [
        ["P101"],
        ["P101", "P202"],
        ["P202", "P101"],
        ["P202", "P101", "P303"],
        ["P202", "P303", "P101"],
        ["P303", "P101", "P202"],
        ["P101", "P202", "P404"],
        ["P202", "P404", "P101"],
    ]
    trace = run_requests()
    assert [step["after"] for step in trace] == expected
    assert trace[-1]["reads"] == 4 and trace[6]["evicted"] == "P303"
    cache = LRUCache(3)
    for key in ("P202", "P404", "P101"):
        cache.put(key, PRODUCTS[key].copy())
    original = cache.nodes["P202"]
    updated = {**PRODUCTS["P202"], "category": "Wireless headphones"}
    cache.put("P202", updated)
    assert cache.nodes["P202"] is original and original.value is updated
    assert cache.order() == ["P404", "P101", "P202"] and len(cache.nodes) == 3
    assert run_requests(tuple(PRODUCTS) * 3)[-1]["reads"] == 12
    fifo, fifo_reads = OrderedDict(), 0
    for key in REQUESTS:
        if key not in fifo:
            fifo_reads += 1
            fifo[key] = PRODUCTS[key]
            if len(fifo) > 3:
                fifo.popitem(last=False)
    assert fifo_reads == 5
    for invalid in (-1, True, 1.5):
        try:
            LRUCache(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid capacity accepted")
    assert implementation_walkthrough() == {
        "request_trace_end": ["P202", "P404", "P101"],
        "structures_end": ["P202", "P101", "P404"],
        "helpers_end": ["P202", "P404", "P101"],
        "get_end": ["P202", "P101", "P404"],
        "update_end": ["P101", "P404", "P202"],
        "insert_end": ["P404", "P202", "P303"],
    }
    rng = Random(42)
    for capacity in (0, 1, 2, 3, 8):
        actual, oracle = LRUCache(capacity), OrderedDict()
        for _ in range(600):
            key = str(rng.randrange(12))
            if rng.random() < 0.6:
                value = {"revision": rng.randrange(10)}
                actual.put(key, value)
                oracle[key] = value
                oracle.move_to_end(key)
                if len(oracle) > capacity:
                    oracle.popitem(last=False)
            elif key in oracle:
                assert actual.get(key) == oracle[key]
                oracle.move_to_end(key)
            else:
                assert actual.get(key) is None
            actual.check()
            assert actual.order() == list(oracle)
    return {
        "requests": trace,
        "database_reads": 4,
        "fifo_database_reads": fifo_reads,
        "oracle_operations": 3000,
        "existing_key_keeps_node": True,
        "no_hit_workload_reads": 12,
    }


if __name__ == "__main__":
    for step in run_requests():
        print(step)
    print(verify())
