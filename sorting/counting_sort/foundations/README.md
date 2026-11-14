# Counting Sort: counts become places

BigOCast | Moein

This is the complete stable Python implementation from the Counting Sort lesson.
The video is in local review; no published video URL is available yet.
Python 3.10 or newer, standard library only.

From the repository root:

```sh
python3 sorting/counting_sort/foundations/counting_sort.py
python3 -m unittest discover -s sorting/counting_sort/foundations -v
```

## Contract and example

`counting_sort(items, K)` takes a list of `(integer_key, payload)` records.
`K` is a nonnegative integer and every key must be in `range(K)`. These are
preconditions, not runtime validation. Negative keys need the offset adaptation
explained below; Python's negative indexing must not be used as that adaptation.

Input: `[(3, "A"), (1, "B"), (3, "C"), (0, "D"), (1, "E")]`, `K=4`.

Expected output: `[(0, "D"), (1, "B"), (1, "E"), (3, "A"), (3, "C")]`.

The letters identify original records. They are carried unchanged, never used
as a secondary sort key. The result contains the same tuple objects, and the
input list remains unchanged. An empty input with `K=0` returns an empty list.

## Why it works

1. Count keys: `[1, 2, 0, 2]`. There is a slot for key 2 even though no record has it.
2. Add left to right: `[1, 3, 3, 5]`. Each running total is the exclusive end of
   its key's group in the output. End 3 sits just after output index 2.
3. Scan original records from right to left. Decrease the record's group end,
   then use that updated value as its destination index.

E takes index 2, D takes 0, C takes 4, B takes 1, and A takes 3. Later equal-key
records take later output slots first, preserving the original order. B remains
before E; A remains before C. Reading forward while still filling from decreasing
ends would reverse equal-key records. A different stable version can read forward
if it uses increasing group starts instead.

## Cost and limits

Time is O(n + K); extra space is O(n + K), including the returned output and
excluding the input. The algorithm allocates K counters and n output references.
It reuses the counter list for group ends and does not copy all payload data.
These bounds assume constant-cost list indexing and integer-key operations.

K counts the supported integer range, including unused keys. Five records with
keys between 0 and 1,000,000 need 1,000,001 counters in this version. A sparse,
wide range can make a comparison sort a better choice.

For negative keys, a separate adaptation can index counters by `key - minimum`
and use `K = maximum - minimum + 1`, while returning the original records.
Finding those bounds adds an O(n) pass. That adaptation is not implemented in
the function shown here.

## Tests and learning checks

Tests cover the exact lesson example, original object identity, unchanged input,
1,093 bounded sequences against Python's stable reference sort, the empty case,
and payload order that differs from alphabetic order.

Try changing the input to `[(1, "Z"), (1, "A"), (0, "Q")]` with `K=2`.
Why must Z stay before A? Why does changing K from 4 to 8 create more counters
without changing the five-card result?

More visual explanations: [bigocast.com](https://bigocast.com).
