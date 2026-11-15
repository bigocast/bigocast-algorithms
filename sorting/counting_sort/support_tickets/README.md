# Counting Sort: support tickets

BigOCast | Moein

This is the complete Python function shown in the support-ticket Counting Sort
lesson. The video is in production; no public video link is available yet.
Python 3.10 or newer, standard library only.

```sh
python3 sorting/counting_sort/support_tickets/counting_sort.py
python3 -m unittest discover -s sorting/counting_sort/support_tickets -v
```

## Input and result

Each ticket is a dictionary with a `subject` and an integer `priority`. Priority
1 comes first. `levels` is a nonnegative integer, and every priority must be in
`1..levels`. These are preconditions, not runtime validation. A missing, negative
or out-of-range priority is outside this function's contract.

The original arrival order is Password reset (2), Payment failed (1), Change photo
(3), App won't open (1), Update email (2). With `levels=3`, the result is:

```text
1 Payment failed
1 App won't open
2 Password reset
2 Update email
3 Change photo
```

Matching priorities keep their arrival order. The result holds the same ticket
objects, including their subjects. The original list and dictionaries are unchanged.

## Counts become positions

The three counters become `[2, 2, 1]`. Adding from left to right changes the same
list to `[2, 4, 5]`. In the hand example, these are the last positions for the
three groups when spaces are numbered 1 to 5.

Python indexes start at zero. Reading the tickets backward, subtract one from a
ticket's group end before placing it. Update email changes the middle counter
from 4 to 3 and takes index 3. Password reset later takes index 2, keeping its
earlier arrival ahead of Update email. The other matching pair stays stable too.

## Cost and limits

For n tickets and K supported priority levels, time is O(n + K). The consecutive
passes add; they are not nested. Extra space is O(n + K), including the returned
result, or O(K) if that returned storage is excluded. The input already exists,
and the result stores references rather than copying every ticket's contents.

K includes priority levels that never appear. Five tickets with priorities from
1 to a million still need a million counters with this function. A wide, sparse
range can make comparison sorting a better choice.

Tests check the exact example, original object identity, unchanged input, empty
input, unused priorities and all 3,280 priority sequences of lengths 0 through 7
against Python's stable reference sort.

More visual lessons: [bigocast.com](https://bigocast.com).
