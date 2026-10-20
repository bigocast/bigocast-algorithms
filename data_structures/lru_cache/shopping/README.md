# How an LRU Cache Decides What to Forget

BigOCast | Moein

This self-contained Python example follows the shopping lesson: Sony, Bose, Sony, AirPods Max, Sony, Bose, Momentum, Sony. Product IDs and the three-record cache are illustrative; this is not a claim about a retailer’s backend.

Requires Python 3.10 or later. No third-party packages.

```sh
python3 data_structures/lru_cache/shopping/lru_cache.py
python3 -m unittest discover -s data_structures/lru_cache/shopping -p 'test_*.py'
```

The trace finishes in least-to-most-recent order `P202, P404, P101`. LRU makes four database reads; FIFO makes five; without caching all eight requests read the source. These are model counts, not speed measurements.

`get(key)` returns the saved dictionary record and promotes its node, or returns `None` on a miss. Records must be dictionaries, so `None` is unambiguous. `put(key, record)` inserts or replaces a record and treats it as recently used. An update preserves the node identity. Capacity zero retains nothing; negative or non-integer capacities are rejected. The dictionary and doubly linked list reference the same nodes. Boundary sentinels do not count toward capacity.

Cache bookkeeping is average/amortized O(1) under ordinary hash-table assumptions. Key hashing and source reads are separate costs. Structural space is O(C) entries, plus record payload bytes. `order()` and `check()` are O(C) inspection helpers, never part of `get` or `put`.

The example is single-threaded. Eviction does not detect stale source data or implement expiry. Try capacity one, capacity zero, an existing-key update, or the four-product cycle at capacity three. The latter has twelve misses over three rounds.

`verify()` compares 3,000 operations against an independent OrderedDict model and checks the demonstrated request counts, links, updates and edge cases. Video link will be added after publication.
