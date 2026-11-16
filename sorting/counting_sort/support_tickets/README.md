# Counting Sort: support tickets

BigOCast | Moein

[Read the tutorial and use the interactive tickets](https://bigocast.com/learn/counting-sort).
The [matching video](https://youtu.be/EdQHMAcq0yc) is scheduled for 23 November 2026,
10:00 UK time. Its link will become playable when released.

## Run

Python 3.10 or newer, standard library only. From the repository root:

```sh
python3 sorting/counting_sort/support_tickets/counting_sort.py
python3 -m unittest discover -s sorting/counting_sort/support_tickets -v
```

Expected subjects in order: Payment failed, App won't open, Password reset,
Update email, Change photo. Priorities are `[1, 1, 2, 2, 3]`.

## Contract

Each ticket is a dictionary with a `subject` and an integer `priority` in
`1..levels`. `levels` must be a nonnegative integer. These are preconditions,
not runtime validation. The function returns a new list containing the original
ticket objects, leaves its input unchanged, and keeps equal priorities in arrival
order. Time and extra space, including the returned list, are O(n + K).

Tests cover the exact video example, object identity, unchanged input, empty
input, unused priorities and all 3,280 priority sequences of lengths 0 through 7.
The Website lesson explains the counts, cumulative totals and reverse placement.

## Short examples

`python3 sorting/counting_sort/support_tickets/short_examples.py` runs the smaller
“Counts become places” and “Why read backward?” inputs. These use the same function
and its one-based priorities, with zero-based Python output indexes. The Shorts
do not yet have public video links.

[More visual lessons from BigOCast](https://www.youtube.com/@bigocast).
