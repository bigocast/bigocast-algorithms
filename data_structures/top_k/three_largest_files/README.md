# Top K: the three largest files

BigOCast | Moein

Keep a min-heap of the largest files seen so far. Once it is full, its minimum
is the admission cutoff. A larger arrival replaces that root; a smaller or equal
arrival leaves the heap unchanged. The heap operation restores parent-child order.

Run from the repository root with Python 3.10 or newer. No dependencies are needed.

```sh
python3 data_structures/top_k/three_largest_files/largest_files.py
python3 -m unittest discover -s data_structures/top_k/three_largest_files -v
```

The exact ten-file video input produces:

```text
project.mov: 150 MB
backup.zip: 140 MB
archive.zip: 120 MB
```

`largest_files(files, k=3)` accepts an iterable of `(size, name)` pairs and returns
up to `k` such pairs in descending order. `k` must be a nonnegative integer;
negative values raise `ValueError`. Zero returns an empty list without consuming
the iterable. If fewer than `k` files exist, all are returned. Sizes are assumed
to be nonnegative finite comparable numbers, and names are strings. No files are
opened, changed or deleted: this example operates on metadata supplied by the caller.

Equal sizes may retain any valid `k` files. Tuple comparison uses the name to
break ties inside the heap, but admission compares only sizes. An arrival equal
to the cutoff is skipped. The input may contain duplicate records.

For positive `k`, every one of the `n` records is inspected. Fixed `k = 3` gives
O(n) scan time. General `k >= 2` gives O(n log k) worst-case scan time; sorting
the retained records adds O(k log k), with O(k) extra space. These are upper
bounds: only `min(n, k)` records can be retained. For `k = 1`, the scan is O(n);
for `k = 0`, it is O(1). An efficient comparison sort of all records takes
O(n log n) worst-case time, and stores the whole input if it arrives as a stream.

Try changing `k` to one, using repeated sizes, reversing the input, or supplying
more records through a generator. The returned top sizes should match a full-sort
oracle even when the retained names at a tied cutoff differ.
