# Bubble Sort in Python

Runnable code for learning Bubble Sort with BigOCast.

For the explanation, worked examples and interactive visualiser, read the
[Bubble Sort tutorial](https://bigocast.com/learn/bubble-sort).
You can also [watch the Bubble Sort video](https://www.youtube.com/watch?v=MadYeOwpZBY).

## Run the example

Use Python 3.10 or newer. No extra packages are needed. From the repository root:

```sh
python3 sorting/bubble_sort/foundations/bubble_sort.py
```

The example sorts `[5, 1, 4, 2, 3]` and prints `[1, 2, 3, 4, 5]`.
Change `numbers` in [bubble_sort.py](bubble_sort.py) to try your own input.

## Use the function

`bubble_sort(numbers, stop_early=True)` changes the supplied list and returns
that same list. Values must be mutually comparable. Empty lists, negative numbers
and duplicates work; equal values keep their original order.

Use `bubble_sort(numbers.copy())` to preserve your input. Set `stop_early=False`
to disable the shortcut that stops after a pass with no swaps. Both modes skip
the final positions settled by earlier passes.

## Run the tests

```sh
python3 -m unittest discover -s sorting/bubble_sort/foundations -v
```

The tests check sorting, in-place return behaviour, equal-item stability and
comparison counts, including the already-sorted and smallest-at-the-end cases.

Find more visual explanations on the [BigOCast YouTube channel](https://www.youtube.com/@bigocast).
