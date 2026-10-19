"""BigOCast | Moein. A bounded application cache around real SQLite queries.

Run this file for the measured request traces. Use --serve for a local read-only
HTTP API. Standard library only. The fixed catalogue does not change during a run.
This is a single-process, sequential teaching service, not a production server.
LRU controls capacity; it supplies neither expiration nor invalidation.

The cache's get/put operations take expected, amortized O(1) time under ordinary
constant-cost hashing/equality. Pathological dictionary collisions can be O(C).
Metadata occupies O(C), plus payload storage. Database work, JSON serialization,
and O(C) diagnostic snapshots are outside the cache-operation bounds.
"""
import argparse
import json
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import NamedTuple


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


class Product(NamedTuple):
    id: int
    name: str
    price_cents: int


PRODUCTS = {
    42: Product(42, "Keyboard", 7900),
    17: Product(17, "Mouse", 2900),
    83: Product(83, "Monitor", 24900),
    91: Product(91, "Dock", 8900),
}
MAIN_REQUESTS = (42, 42, 17, 83, 42, 91, 42, 17)
CYCLE_REQUESTS = (42, 17, 83, 91) * 2
SHORT_REQUESTS = {
    "caching": (42, 42),
    "hit_miss": (42, 17, 42, 83, 17),
    "eviction": (42, 17, 83, 42, 91),
    "lookup": (42, 17, 83, 17),
    "reorder": (42, 17, 83, 17),
    "all_misses": CYCLE_REQUESTS,
}


class ProductStore:
    """Fixed catalogue. The trace callback records executed SELECT statements."""

    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        self.db.execute(
            "CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price_cents INTEGER)"
        )
        self.db.executemany("INSERT INTO products VALUES (?, ?, ?)", PRODUCTS.values())
        self.db.commit()
        self.selects = []
        self.db.set_trace_callback(self._record_select)

    def _record_select(self, sql):
        if sql.lstrip().upper().startswith("SELECT "):
            self.selects.append(sql)

    def fetch(self, product_id):
        row = self.db.execute(
            "SELECT id, name, price_cents "
            "FROM products WHERE id = ?",
            (product_id,),
        ).fetchone()
        if row is None:
            raise KeyError(product_id)
        return Product(*row)

    def close(self):
        self.db.close()


class ProductAPI:
    def __init__(self, store, capacity=3):
        self.store = store
        self.cache = LRUCache(capacity)

    def get_product(self, product_id):
        try:
            return self.cache.get(product_id)
        except KeyError:
            product = self.store.fetch(product_id)
            self.cache.put(product_id, product)
            return product

    def handle_get(self, path):
        """A deliberately narrow HTTP route; errors never populate the cache."""
        prefix = "/products/"
        token = path[len(prefix):] if path.startswith(prefix) else ""
        if not token or not token.isascii() or not token.isdecimal():
            return 404, {"error": "Product not found"}
        # Bound parsing before int conversion, including maliciously long IDs.
        if len(token) > 9:
            return 404, {"error": "Product not found"}
        try:
            product = self.get_product(int(token))
        except KeyError:
            return 404, {"error": "Product not found"}
        return 200, product._asdict()


def request_trace(requests=MAIN_REQUESTS, capacity=3):
    """Execute the route and SQLite reads; snapshots cost O(n * capacity)."""
    store = ProductStore()
    api = ProductAPI(store, capacity)
    steps = []
    hits = misses = 0
    try:
        for key in requests:
            if isinstance(key, bool) or not isinstance(key, int) or key not in PRODUCTS:
                raise ValueError("Use product IDs 42, 17, 83 and 91.")
            before = [item[0] for item in api.cache.items()]
            queries_before = len(store.selects)
            status, product = api.handle_get(f"/products/{key}")
            assert status == 200
            hit = len(store.selects) == queries_before
            hits += int(hit)
            misses += int(not hit)
            evicted = before[0] if not hit and len(before) == capacity else None
            order = [item[0] for item in api.cache.items()]
            steps.append({
                "key": key, "product": product, "hit": hit, "evicted": evicted,
                "order": order, "hits": hits, "misses": misses,
                "queries": len(store.selects),
                "sql": None if hit else store.selects[-1],
            })
        return {"capacity": capacity, "hits": hits, "misses": misses,
                "queries": len(store.selects), "steps": steps}
    finally:
        store.close()


def experiment(inputs):
    if any(not isinstance(inputs.get(name), str) or len(inputs[name]) > 200
           for name in ("capacity", "requests")):
        raise ValueError("Inputs must be text fields of at most 200 characters.")
    capacity = inputs["capacity"].strip(" \t\r\n")
    if capacity not in {"1", "2", "3", "4"}:
        raise ValueError("Choose a capacity from 1 to 4.")
    keys = [part.strip(" \t\r\n") for part in inputs["requests"].split(",")]
    if not 1 <= len(keys) <= 20 or any(key not in {"42", "17", "83", "91"} for key in keys):
        raise ValueError("Enter 1 to 20 product IDs: 42, 17, 83 or 91.")
    return request_trace([int(key) for key in keys], int(capacity))


def parity_cases():
    examples = [(MAIN_REQUESTS, 3), (CYCLE_REQUESTS, 3), (CYCLE_REQUESTS, 4),
                ((42, 42, 17, 17, 42), 1), (SHORT_REQUESTS["hit_miss"], 3), ((83,), 2)]
    return [{"input": {"capacity": str(capacity), "requests": ",".join(map(str, keys))},
             "expected": request_trace(keys, capacity)} for keys, capacity in examples]


def verify():
    main = request_trace()
    assert [step["order"] for step in main["steps"]] == [
        [42], [42], [42, 17], [42, 17, 83], [17, 83, 42],
        [83, 42, 91], [83, 91, 42], [91, 42, 17],
    ]
    assert (main["hits"], main["queries"]) == (3, 5)
    assert request_trace(CYCLE_REQUESTS)["queries"] == 8
    assert request_trace(CYCLE_REQUESTS, 4)["queries"] == 4
    assert request_trace((42, 42))["queries"] == 1
    store = ProductStore()
    try:
        assert store.fetch(42) == store.fetch(42) == PRODUCTS[42]
        assert len(store.selects) == 2
    finally:
        store.close()
    return {"uncached_repeated_queries": 2, "cached_repeated_queries": 1,
            "main_hits": 3, "main_queries": 5, "cycle_queries": 8, "four_slot_queries": 4}


def serve(port=8000):
    """Sequential loopback demo. Cache persists across requests to this process."""
    store = ProductStore()
    api = ProductAPI(store)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            status, result = api.handle_get(self.path)
            data = json.dumps(result).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("X-Database-Queries", str(len(store.selects)))
            self.end_headers()
            self.wfile.write(data)

    try:
        with HTTPServer(("127.0.0.1", port), Handler) as server:
            print(f"Read-only demo: http://127.0.0.1:{server.server_address[1]}/products/42", flush=True)
            server.serve_forever()
    finally:
        store.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if args.serve:
        serve(args.port)
    else:
        print(json.dumps({"checks": verify(), "main": request_trace(),
                          "cycle_three": request_trace(CYCLE_REQUESTS),
                          "cycle_four": request_trace(CYCLE_REQUESTS, 4)}, indent=2))
