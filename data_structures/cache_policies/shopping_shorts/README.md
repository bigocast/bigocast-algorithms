# Cache Lab: seven standalone shopping examples

BigOCast | Moein

Runnable Python companions for seven Shorts: caching and hits/misses, LRU, FIFO,
LFU, comparing those three rules, cache thrashing, and stale-price invalidation.
Each example starts from its own empty cache. No long lesson or previous example
is required. The shopping app, product IDs and prices are illustrative.

Python 3.10 or newer; standard library only. From the repository root:

```sh
python3 data_structures/cache_policies/shopping_shorts/cache_lab.py
python3 data_structures/cache_policies/shopping_shorts/cache_lab.py lfu --trace
python3 data_structures/cache_policies/shopping_shorts/cache_lab.py freshness --trace
python3 -m unittest discover -s data_structures/cache_policies/shopping_shorts -v
```

The first command prints:

```text
caching: 3 requests, 1 hit, 2 database reads
lru: 5 requests, 1 hit, 4 database reads; last removed Bose
fifo: 5 requests, 1 hit, 4 database reads; last removed Sony
lfu: 7 requests, 3 hits, 4 database reads; last removed Bose
comparison: FIFO removes Sony; LRU removes Bose; LFU removes Bose
thrashing: 8 requests, 0 hits, 8 database reads; last removed Sony
freshness: first $300; stale hit $300; after invalidation $250; 2 database reads
```

Pass any example name in the table below to run it alone. `--trace` also prints
each request's hit/miss, removed product, source-read total and saved records.

## Exact examples

The product map is `P101: Sony`, `P202: Bose`, `P303: AirPods`, `P404: Momentum`.
The source database is represented by a Python dictionary; counts are simulated
reads, not latency measurements or real network requests.

| Example | Complete request sequence | Result |
| --- | --- | --- |
| `caching` | Sony, Sony, Bose | Miss, hit, miss: two source reads for three requests. |
| `lru` | Sony, Bose, AirPods, Sony, Momentum | Sony becomes most recently used; Bose is removed for Momentum. |
| `fifo` | Sony, Bose, AirPods, Sony, Momentum | Reusing Sony leaves its arrival order unchanged; Sony is removed for Momentum. |
| `lfu` | Sony, Bose, AirPods, Sony, Sony, AirPods, Momentum | Sony has three uses, Bose one, AirPods two. Remove Bose; Momentum starts at one. |
| `comparison` | The same seven-request sequence as LFU, independently for each rule | FIFO removes Sony; LRU and LFU both remove Bose, for different reasons. |
| `thrashing` | Sony, Bose, AirPods, Momentum, then that same sequence again | Three slots cannot retain this four-product loop: eight misses, eight reads. |
| `freshness` | Read Sony at $300; change source to $250; read saved copy; invalidate; read again | The hit still returns $300. Only the visit after invalidation fetches $250. |

The freshness example uses a plain dictionary of saved copies. It does not depend
on an eviction policy. Removing a stale copy does not update it or fetch data;
the next visit performs the new read. In a real app something must trigger
invalidation; this example performs it explicitly and does not detect source changes.

## Contract and rules

- `Cache(policy, capacity)` accepts `fifo`, `lru` or `lfu` and a positive integer
  entry count. Zero, negative, boolean and non-integer capacities are rejected.
- `request(key, source)` returns an independent snapshot after serving the request.
  A missing copy is loaded from `source`; a full cache removes a resident before
  inserting the new copy. A hit returns the saved value without consulting `source`.
  An unknown source key on a miss raises `KeyError` without changing cache state.
- Source values and diagnostic outputs are copied, so later source edits and edits
  to returned snapshots cannot silently update saved values. Keys must be hashable.
- FIFO means **first in, first out**: use arrival order. Hits do not alter arrival.
- LRU means **least recently used**: use last access. A successful hit is a use.
- LFU means **least frequently used**: count the initial fetch and each subsequent
  hit while a copy is stored. A removed copy loses its count; re-entry starts at one.
  Equal counts use least recent access as the tie rule. The video's unequal counts
  do not exercise this tie, but the implementation and tests make the choice explicit.
- Every comparison branch starts from a fresh cache, receives the identical request
  history and counts its own reads. Matching removal choices do not make the rules
  equivalent. No rule is claimed to be universally best.

## Costs and limits

This is a teaching simulator, not the linked-list implementation from the long
LRU lesson. At capacity C, finding a removal candidate scans at most C entries,
so a full miss costs O(C) policy work. The actual dictionary hit and counter updates
are expected O(1) under ordinary hash-table assumptions. Every returned diagnostic
snapshot additionally copies C records and sorts their recent-use order in
O(C log C) time. A trace of n requests therefore costs O(n C log C) time and O(n C)
output space when record payload sizes are bounded. Deep-copy cost grows with payload
size. The live cache stores O(C) records. Source I/O is outside these bookkeeping costs.

There is no concurrency, byte-size accounting, automatic expiry or production
database integration. The examples isolate the mechanism shown in each Short.

## Useful changes

- Run `trace("lru", tuple(PRODUCTS) * 2, capacity=4)` in Python: the first four
  requests miss and the next four hit. This answers the thrashing Short's final question.
- Change the request order to see where FIFO, LRU and LFU choose different products.
- Use capacity one to make every switch replace the only saved copy.
- Change the source price again before invalidation to inspect the stale hit.

The tests cover every demonstrated result, LFU ties and count reset, one-slot
operation, rejected capacities, safe snapshots, missing products and 3,600
requests checked against a separate request-history oracle.

Video links will be added after publication.
