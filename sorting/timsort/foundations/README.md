# Timsort ideas: run-and-merge model

This is an intentionally small **run-and-merge teaching model**, not a complete Timsort implementation. It detects natural runs, extends short ones with binary insertion and merges adjacent pairs. It does not use the production merge policy or galloping. Use Python `sorted()` or `list.sort()` in application code.

[Read the tutorial and try the visualiser](https://bigocast.com/learn/timsort).

Returns a new list and leaves the input unchanged. The teaching minimum run length must be positive.

## Run

From the repository root:

```sh
python3 sorting/timsort/foundations/run_merge_sort.py
python3 sorting/timsort/foundations/stable_records.py
python3 -m unittest discover -s sorting/timsort/foundations -v
```

The example prints `[1, 2, 3, 4, 5, 6, 7, 8, 9]`. Tests cover empty input, duplicates, reverse order and exhaustive small lists.

[More visual lessons on BigOCast](https://www.youtube.com/@bigocast).

`stable_records.py` is the built-in `sorted()` / `list.sort()` example shown in the article.
