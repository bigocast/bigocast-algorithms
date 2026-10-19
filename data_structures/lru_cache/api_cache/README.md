# LRU Cache: From Hits and Misses to Python

BigOCast | Moein

A runnable cache around real SQLite queries. The current foundations lesson uses
six requests: `42, 42, 17, 83, 42, 91`. The first request for 42 reads and caches
the keyboard record; the next request reuses it. Later, reusing 42 protects it
from eviction, so adding 91 removes 17. The cache is a dictionary plus a doubly
linked list, with room for three products.

This folder also preserves the earlier eight-request API lesson and its optional
HTTP server. Both examples use the same cache implementation.

Python 3.10 or newer; standard library only. The video package is in production;
no video URL is available yet.

## Run the six-request lesson

From the repository root:

```sh
python3 data_structures/lru_cache/api_cache/run_example.py
```

This starts a fresh cache and in-memory database. Its exact output is:

```text
42  MISS   Keyboard  reads=1
42  HIT    Keyboard  reads=1
17  MISS   Mouse     reads=2
83  MISS   Monitor   reads=3
42  HIT    Keyboard  reads=3
91  MISS   Dock      reads=4
LRU to MRU: [83, 42, 91]
```

There are two hits and four database reads. The last line lists cached keys from
least to most recently used. A hit returns before the database call, and evicting
a cached record leaves the original database row intact.

## Run the earlier API examples and tests

The earlier eight-request trace, cycle comparisons and checks remain available:

```sh
python3 data_structures/lru_cache/api_cache/api_cache.py
python3 -m unittest discover -s data_structures/lru_cache/api_cache -v
```

The first command creates fresh in-memory SQLite databases for the examples and
prints each request, actual SELECT statement, eviction, recency order, and running
query count. Its checks report:

```json
{
  "uncached_repeated_queries": 2,
  "cached_repeated_queries": 1,
  "main_hits": 3,
  "main_queries": 5,
  "cycle_queries": 8,
  "four_slot_queries": 4
}
```

To make real HTTP requests, start the local server:

```sh
python3 data_structures/lru_cache/api_cache/api_cache.py --serve --port 8000
```

Then run these in a second terminal:

```sh
curl -i http://127.0.0.1:8000/products/42
curl -i http://127.0.0.1:8000/products/42
```

Both return `{"id": 42, "name": "Keyboard", "price_cents": 7900}`. On a fresh
server, both responses include `X-Database-Queries: 1`. That header counts SELECT
statements executed since this server started. Stop with Ctrl+C; restarting gives
you a fresh database, cache, and counter. Use another port if 8000 is occupied, or
`--port 0` to select an available port and print its actual URL.

## Catalogue and request examples

| Product ID | Name | Price in cents |
| --- | --- | --- |
| 42 | Keyboard | 7900 |
| 17 | Mouse | 2900 |
| 83 | Monitor | 24900 |
| 91 | Dock | 8900 |

Each row below starts with an empty cache and a fresh database. Recency orders run
from least recently used to most recently used.

| Example | Capacity | Requests | Result |
| --- | --- | --- | --- |
| Current foundations lesson | 3 | 42, 42, 17, 83, 42, 91 | 2 hits, 4 queries; final order 83, 42, 91 |
| Earlier API lesson | 3 | 42, 42, 17, 83, 42, 91, 42, 17 | 3 hits, 5 queries; final order 91, 42, 17 |
| General caching | 3 | 42, 42 | 1 hit, 1 query; one record serves both requests |
| Hit and miss | 3 | 42, 17, 42, 83, 17 | 2 hits, 3 queries; 2/5 = 40% hits |
| Eviction | 3 | 42, 17, 83, 42, 91 | Product 17 is evicted; final order 83, 42, 91 |
| Direct lookup | 3 | 42, 17, 83, 17 | Product 17 is found by key; final order 42, 83, 17 |
| Reordering | 3 | 42, 17, 83, 17 | The same product-17 node moves from middle to most recent |
| Four-product cycle | 3 | 42, 17, 83, 91, 42, 17, 83, 91 | 0 hits, 8 queries |
| Same cycle with four slots | 4 | 42, 17, 83, 91, 42, 17, 83, 91 | First four miss; next four hit; 4 queries |

`run_example.py` runs the six requests from the current foundations lesson.
`MAIN_REQUESTS` preserves the earlier eight-request example; `CYCLE_REQUESTS`
and `SHORT_REQUESTS` contain the other inputs above.
`request_trace(requests, capacity)` executes the application route and SQLite
queries. The HTTP server always uses capacity 3; the Python function lets you
compare other capacities. From this example's folder, try:

```python
from api_cache import request_trace

print(request_trace((42, 17, 42, 17, 42, 17), 2))  # 4 hits, 2 queries
print(request_trace((42, 17, 42), 1))              # 0 hits, 3 queries
```

## Application contract

The service binds only to `127.0.0.1` and handles requests sequentially in one
process. It is a small teaching server. Its database contains the four fixed
records above and has no write route.

`GET /products/<id>` accepts one to nine ASCII digits. Leading zeros refer to the
same integer ID, so `/products/0042` can hit the entry for 42. Query strings,
extra path segments, encoded IDs, signs, and non-ASCII digits are outside this
route's contract and return 404 without a query. A valid numeric ID absent from
the catalogue executes a SELECT and returns 404. Errors are not cached and do not
evict or reorder valid cached products. Unsupported HTTP methods use the standard
handler's 501 response.

On a miss, `ProductAPI` fetches the record before changing the cache. A missing
record or database failure therefore leaves existing entries intact. A successful
fetch becomes the most recent entry. A hit also makes its entry most recent.
Eviction removes a cached record reference; the SQLite row remains available.

`Product` is an immutable named tuple whose fields are integers and a string.
The cache stores that record, not a complete HTTP response. `handle_get` makes a
new dictionary and the handler serializes JSON on every request, including hits.
There is no TTL, invalidation, locking, shared cache across processes, or promise
of freshness if the database changes. LRU decides which entry to evict when full.

## Cache contract and costs

- `LRUCache(capacity)` requires a positive integer entry count; booleans and
  non-integers raise `ValueError`.
- `get(key)` returns the stored value and promotes the same node. A missing key
  raises `KeyError` without changing the cache.
- `put(key, value)` inserts or updates and makes the entry most recent. Updating
  uses no extra slot. A new key at capacity evicts the least recent entry.
- Keys must have stable hash/equality behavior. Generic cache values are object
  references; `None` is a valid key or value. The application uses integer keys
  and immutable `Product` values.
- `items()` returns a diagnostic list of pairs from least to most recent. The
  head and tail markers are not entries and do not consume capacity.

Cache `get` and `put` take expected, amortized O(1) time under ordinary
constant-cost hashing and equality. Reference changes take a fixed number of
steps. Pathological dictionary collisions can take O(C), where C is capacity;
custom hashing, equality, and payload destruction can have their own costs.
Cache metadata occupies O(C), plus retained payload memory. Capacity counts
entries, not bytes.

Database work and per-request JSON serialization are outside those cache bounds.
`items()` costs O(C) time/output space; recording every order for n requests costs
O(nC) time/output space. The teaching store also retains an O(Q) SQL trace for Q
executed SELECTs. The entire instrumented process is therefore not bounded to
O(C) memory.

SQLite's trace callback counts statements actually executed. The database here
is in memory: these counts are not physical disk reads or timing measurements.
The example introduces no artificial delay and claims no measured speedup.

LRU uses recent access as a prediction. The four-product/three-slot cycle shows a
workload where that prediction produces no hits. The tests check both link
directions, compare 2,000 mixed operations with an independent `OrderedDict`
oracle, exercise real SQLite reads and errors, and make actual requests to a
temporary HTTP subprocess.
