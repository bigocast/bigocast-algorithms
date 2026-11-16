# Bucket Sort

[Read the tutorial and try the visualiser](https://bigocast.com/learn/radix-sort).

Returns a new list and leaves the input unchanged. Accepts integers from 0 to 99 and a positive bucket count. Memory grows with the bucket count.

## Run

From the repository root:

```sh
python3 sorting/bucket_sort/foundations/bucket_sort.py
python3 -m unittest discover -s sorting/bucket_sort/foundations -v
```

The example prints `[7, 12, 31, 42, 76, 95]`. Tests cover empty input, duplicates, reverse order and exhaustive small lists.

[More visual lessons on BigOCast](https://www.youtube.com/@bigocast).
