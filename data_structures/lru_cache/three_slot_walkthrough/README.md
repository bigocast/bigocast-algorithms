# How an LRU Cache Decides What to Forget

BigOCast | Moein

Follow the three-slot shopping walkthrough: Sony, Bose, Sony, AirPods, Sony, Bose,
Momentum, Sony. This is an illustrative application using real product names.

Requires Python 3.10 or later and only the standard library.

```sh
python3 data_structures/lru_cache/three_slot_walkthrough/lru_cache.py
python3 -m unittest discover -s data_structures/lru_cache/three_slot_walkthrough -v
```

The trace ends in least-to-most-recent order `P202, P404, P101`. LRU needs four
source reads; FIFO needs five; uncached access needs eight. These are counts for
this exact request sequence, not measured speedups.

`get(key)` returns a saved dictionary record and makes its node most recent, or
returns `None` without changing the list. `put(key, record)` updates an existing
node in place, or evicts the least recent entry before inserting a new node when
full. Reads and writes both count as uses. The dictionary references the same
objects as the linked list. The two empty boundary nodes use no product slots.

`implementation_walkthrough()` reproduces every order shown beside the Python
code, including helper calls, a miss, a node-preserving value update and eviction
from both structures. Capacity zero keeps nothing. Negative, non-integer and
boolean capacities are invalid. Record values must be dictionaries, so `None`
unambiguously means a miss.

Cache bookkeeping is average/amortized O(1), assuming ordinary hash-table
behaviour and constant-cost key hashing. Source reads are separate. Space is
O(C) structural entries, plus the actual record bytes. `order()` and `check()`
are O(C) inspection helpers, never called by `get` or `put`.

The implementation is single-threaded and does not provide expiry, invalidation
or protection against a caller mutating a returned record. LRU tracks recent
use; it does not guarantee freshness or a hit. Try the four-product cycle with
capacity three: all twelve requests miss across three rounds. Also try capacity
one, zero, a missing key and an existing-key update.

The tests check the video states, identity, both structures, a 3,000-operation
independent OrderedDict oracle, and the capacity limit during insertion.
The video link will be added after publication.
