# Bloom Filter: a few bits can skip a database read

BigOCast | Moein

The complete Python implementation for **Bloom Filters Explained: Skip Database
Reads with a Few Bits**, with the examples from its two Shorts: **One Zero Can
Save a Database Read** and **The Bloom Filter Deletion Trap**.

## Run the example

Use Python 3.10 or newer. No third-party packages are needed. From the repository root:

```sh
python3 data_structures/bloom_filter/foundations/bloom_filter.py
```

Start with [bloom_filter.py](bloom_filter.py). It contains:

- `BloomFilter`: the readable list-based implementation taught in the video.
- `PackedBloomFilter`: the same operations using a packed byte array.
- `sizing(n, p)`: the approximate number of bits and hashes for a planned capacity.
- A runnable example with the exact words, hashes and queries from the lesson.

## The exact lesson example

Create a filter with 12 logical bits and 3 hashes, then insert `dog` and `pig`.

| Word | Hash positions | Was it inserted? | Query result |
| --- | --- | --- | --- |
| `dog` | 9, 3, 10 | Yes | Possibly present |
| `pig` | 8, 9, 1 | Yes | Possibly present |
| `elk` | 8, 1, 7 | No | Definitely absent |
| `rat` | 8, 10, 3 | No | Possibly present, a false positive |

After both insertions, the logical array is:

```text
[0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0]
```

The hash procedure is repeatable: encode `seed:item` as UTF-8, compute SHA-256,
interpret the first eight digest bytes as a big-endian integer, then take the
remainder modulo `m`. Seeds range from zero through `k - 1`. These are real hash
results, not hand-picked positions supplied by a lookup table.

## What the answers mean

`add(item)` sets every hashed position to one. `might_contain(item)` returns:

- `False` when any position is zero: the item was not inserted.
- `True` when all positions are one: check the authoritative set or database.

Use string items and positive integer values for `m` and `k`. The constructors
reject invalid sizes and hash counts with `ValueError`. The filter does not store
the original items and cannot enumerate them or give an exact membership answer.

Inserted items are not rejected when insertions have completed, the same hashes
and parameters are used, and bits have not been cleared or lost. Reinserting an
item leaves the filter unchanged. More distinct insertions tend to set more bits
and increase false positives. A completely full filter answers `True` to everything.

## Why ordinary deletion breaks the guarantee

Run the separately labeled failure example:

```sh
python3 data_structures/bloom_filter/foundations/unsafe_deletion.py
```

It inserts `dog` and `pig`, then deliberately clears pig's positions. Both words
use bit 9, so querying `dog` now returns `False` even though dog was never removed.
The example demonstrates the bug from the Short; it is not a supported deletion
method. Neither class has a removal API. Counting Bloom filters require a different
design and rules.

## Memory, time and sizing

Insertion performs `k` hashes and bit writes. A query performs at most `k` hashes
and probes, stopping at the first zero. These are `O(k)` operations if hashing an
item is treated as constant cost. With variable-length strings, account for the
cost of hashing their encoded bytes for each seed; longer strings are not free.

The logical filter uses `m` bits. The readable version uses `m` Python list slots,
which consume more than `m` bits. The packed array occupies `ceil(m / 8)` bytes,
plus Python object and parameter overhead. Construction initializes the array;
its work grows with the storage allocated. Insertion and queries do not keep an
exact set alongside it. Hashing temporarily allocates the encoded item and digest.

`sizing(n, p)` takes a positive integer planned item count and a numeric target
false-positive rate strictly between zero and one. It uses the usual approximation:

```text
m = ceil(-n * ln(p) / ln(2)^2)
k = max(1, round((m / n) * ln(2)))
```

For one million items and a target rate of 1%, it returns **9,585,059 bits and 7
hashes**. The packed array needs **1,198,133 bytes** before bookkeeping. This is a
sizing estimate under well-distributed hash assumptions, not a measured guarantee
for arbitrary inputs. A 1% false-positive rate is not the probability that an
item is absent after a positive answer. Changing `m` or `k` after insertion makes
the stored bits inconsistent with future queries; build a new filter instead.

## Try it

- Add `rat`, then query it again. The bits and result stay the same, but it is now
  actually inserted. The filter cannot tell those two situations apart.
- Insert more words into the 12-bit filter and observe which zero bits disappear.
- Replace `BloomFilter` with `PackedBloomFilter` and compare query answers.
- Choose a larger planned capacity with `sizing`, construct a new filter and insert
  the same items again.

These implementations are teaching examples. They do not provide concurrency,
persistence or the engineering of a production Bloom-filter library.

## Run the checks

```sh
python3 -m unittest discover -s data_structures/bloom_filter/foundations -v
```

The tests cover the video's exact hashes and bit states, its real false positive,
definite absence, no false negatives after completed insertions, repeated inserts,
packed/list equivalence across byte boundaries, Unicode strings, invalid parameters,
the sizing example and the deliberately unsafe deletion.
