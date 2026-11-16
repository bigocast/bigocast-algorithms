"""Quicksort and Quickselect using a last-value Lomuto partition.

BigOCast | Moein

Tutorial and visualiser: https://bigocast.com/learn/quick-sort
YouTube channel: https://www.youtube.com/@bigocast
Video: https://youtu.be/gQvo6zioDfw
Scheduled for 17 November 2026, 10:00 UK time.

All functions rearrange the supplied list. Bounds are inclusive and comparisons
use strict <. This teaching version is not stable and has O(n**2) worst-case time.
Quicksort also has O(n) worst-case recursion depth; use Python's built-in sort
for large production inputs.
"""

def partition(a, lo, hi):
    pivot = a[hi]
    boundary = lo
    for scan in range(lo, hi):
        if a[scan] < pivot:
            a[boundary], a[scan] = a[scan], a[boundary]
            boundary += 1
    a[boundary], a[hi] = a[hi], a[boundary]
    return boundary


def quicksort(a, lo=0, hi=None):
    if hi is None:
        hi = len(a) - 1
    if lo >= hi:
        return
    p = partition(a, lo, hi)
    quicksort(a, lo, p - 1)
    quicksort(a, p + 1, hi)


def quickselect(a, k, order="smallest"):
    if type(k) is not int or not 1 <= k <= len(a):
        raise ValueError("k must be an integer in 1..len(a).")
    if order not in ("smallest", "largest"):
        raise ValueError("order must be smallest or largest.")
    target = k - 1 if order == "smallest" else len(a) - k
    lo, hi = 0, len(a) - 1
    while lo < hi:
        p = partition(a, lo, hi)
        if p == target:
            return a[p]
        if target < p:
            hi = p - 1
        else:
            lo = p + 1
    return a[lo]


if __name__ == "__main__":
    original = [7, 2, 9, 4, 3, 8, 5]
    values = original.copy()
    quicksort(values)
    print("Sorted:", values)
    print("Third smallest:", quickselect(original.copy(), 3))
    print("Second largest:", quickselect(original.copy(), 2, "largest"))
