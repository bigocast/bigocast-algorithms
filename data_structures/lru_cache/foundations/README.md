# LRU Cache: Which Picture Should We Forget?

BigOCast | Moein

A complete dictionary-and-doubly-linked-list implementation, with the picture-cache
examples used in the long lesson and six standalone Shorts. Python 3.10 or newer;
standard library only. The video package is in production; no video URL is available yet.

From the repository root:

```sh
python3 data_structures/lru_cache/foundations/lru_cache.py
python3 -m unittest discover -s data_structures/lru_cache/foundations -v
```

## Cache contract

- `LRUCache(capacity)` requires a positive integer entry count; zero, negative,
  boolean and non-integer capacities raise `ValueError`.
- `put(key, value)` inserts or updates an entry and makes it most recently used.
  Updating keeps the same node and does not use an extra slot. A new key at capacity
  evicts the least recently used entry before insertion.
- `get(key)` returns the stored value and makes that entry most recent. A missing
  key raises `KeyError` without changing the cache. The caller fetches missing data
  and calls `put`; a miss does not automatically insert anything.
- Keys must be hashable with stable hash/equality behavior. Values are references
  to Python objects, not copies. `None` is a valid key or value.
- `items()` returns a diagnostic list of `(key, value)` pairs from least to most
  recent. The head and tail markers are not cache entries and do not use capacity.
- This teaching implementation does not provide locking, expiration or freshness
  invalidation. Removing a cached reference does not delete an original source file.

## Reproduce the examples

Picture IDs are `10: cat`, `20: lake`, `30: tree`, `40: boat`.

| Example | Capacity | Requests | Expected result |
| --- | --- | --- | --- |
| Long lesson | 3 | cat, lake, tree, cat, boat, cat, lake | 2 hits, 5 misses; final order boat, cat, lake |
| General caching Short | 2 | cat, cat | 1 hit, 1 miss; one source fetch serves two requests |
| Hit/miss Short | 3 | cat, lake, cat, tree, lake | 2 hits, 3 misses; 2/5 = 40% hits |
| Eviction Short | 3 | cat, lake, tree, cat, boat | Lake is evicted; final order tree, cat, boat |
| Direct lookup Short | 3 | cat, lake, tree, lake | Key 20 returns lake; final order cat, tree, lake |
| Reordering Short | 3 | cat, lake, tree, lake | The same lake node moves from middle to most recent |
| All-miss Short and long chapter | 3 | cat, lake, tree, boat, cat, lake, tree, boat | 0 hits, 8 misses |
| Same cycle with room for all four | 4 | cat, lake, tree, boat, cat, lake, tree, boat | First four miss; next four hit |

The demo prints every request, victim, recency order and cumulative result. `PICTURES`
is a stand-in for an original source; `request_trace` is the caller that loads on misses.
The lookup and reordering Shorts teach different operations using the same small input.

Try `request_trace((10, 20, 10, 20, 10, 20), 2)` for useful repeated reuse, or
`request_trace((10, 20, 10), 1)` to see a one-slot cache replace its only entry.
For update behavior, put cat and lake, then `put(10, "updated cat")`: the cat moves
last, its payload changes, and the cache still has two entries.

## Cost and limitations

`get` and `put` have expected, amortized O(1) time with constant-cost hashing and
equality. The list uses a fixed number of reference updates. Dictionary collisions
can produce O(C) work for capacity C; arbitrary user-defined hashing/equality or
payload destruction can have their own costs. The metadata is O(C), plus retained
payload memory. Capacity counts entries, not bytes. Source fetching, computation
and copying are outside these cache-operation bounds.

`items()` costs O(C) time/output space. The diagnostic request trace deliberately
copies every order, so n requests take O(nC) time/output space in that demonstration.
That instrumentation is separate from the cache operations being taught.

LRU uses the recent past as a prediction. It is not an optimal policy for every
workload. The four-picture/three-slot cycle demonstrates that limitation concretely.
Python's `collections.OrderedDict` provides explicit order updates, and
`functools.lru_cache` provides bounded function memoization. The custom implementation
here makes the mechanism inspectable; it is not a requirement for every application.

The tests compare 2,000 mixed operations against an independent `OrderedDict` oracle,
check both link directions, and cover updates, missing keys, one-slot capacity,
node identity and the demonstrated traces.
