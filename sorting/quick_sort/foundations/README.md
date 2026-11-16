# Quick Sort and Quickselect

The runnable Python companion to [BigOCast’s Quick Sort lesson](https://bigocast.com/learn/quick-sort).
Use the lesson for the worked example, interactive partition and call tree.
[BigOCast on YouTube](https://www.youtube.com/@bigocast) has more visual explanations;
the [matching Quick Sort video](https://youtu.be/gQvo6zioDfw) is scheduled for
17 November 2026, 10:00 UK time. Its link becomes playable after release.
The partition uses the video’s `a`, `lo`, `hi`, `boundary` and `scan` names.
Default bounds are a convenience; Quickselect is an extension beyond the video.

## Run it

Python 3.10 or newer, standard library only. From the repository root:

```sh
python3 sorting/quick_sort/foundations/quick_sort.py
python3 -m unittest discover -s sorting/quick_sort/foundations -v
```

Expected results: sorted `[2, 3, 4, 5, 7, 8, 9]`, third smallest `4`, second largest `8`.

## Use it

- `quicksort(values)` changes the original list and returns `None`.
- `partition(values, lo, hi)` uses inclusive bounds and the last value as pivot.
  It returns the pivot’s final index; the two sides can still be unsorted.
- `quickselect(values, k, order="smallest")` returns the kth occurrence, counting
  from 1. Use `order="largest"` for descending rank. It also rearranges the list.
  Invalid ranks and unknown orders raise `ValueError`.

Pass a copy if you need to preserve the input. The functions assume mutually
comparable values; a direct partition call needs a valid nonempty range.

This is the lesson’s strict-`<`, fixed-pivot variant. It is not stable. Sorted
or all-equal inputs can take O(n²) time. Quicksort’s stack is O(log n) with balanced
splits and O(n) in the worst case; large bad inputs can hit Python’s recursion limit.
Quickselect here uses O(1) auxiliary space. Tests check exhaustive small inputs,
rank selection with duplicates, partition boundaries and the exact lesson example.
