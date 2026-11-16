# Counting Sort

The runnable Python companion to [BigOCast’s Counting Sort lesson](https://bigocast.com/learn/counting-sort).
The lesson explains the counts, running totals and backward placement with an
adjustable visual lab. [BigOCast on YouTube](https://www.youtube.com/@bigocast)
has more visual explanations; this lesson’s matching video is not public yet.

## Run it

Python 3.10 or newer, standard library only. From the repository root:

```sh
python3 sorting/counting_sort/foundations/counting_sort.py
python3 -m unittest discover -s sorting/counting_sort/foundations -v
```

Input: `[(3, "A"), (1, "B"), (3, "C"), (0, "D"), (1, "E")]`, with `K=4`.
Output: `[(0, "D"), (1, "B"), (1, "E"), (3, "A"), (3, "C")]`.

## Use it

`counting_sort(items, K)` returns the original `(integer_key, payload)` records
in key order, leaving the input list unchanged. Equal keys retain their input
order. Payloads are carried along, never used as secondary sort keys.

`K` must be a nonnegative integer and every key must satisfy `0 <= key < K`.
These are preconditions, not runtime validation. Negative keys need an offset
adaptation; Python’s negative indexing is not that adaptation. Empty input with
`K=0` returns an empty list.

Time and extra space, including output, are O(n + K). A wide key range can make
this a poor choice even for a short input. Tests check the worked example,
original record identity, unchanged input, stability and 1,093 small sequences.
See the linked tutorial for the explanation and negative-key extension.
