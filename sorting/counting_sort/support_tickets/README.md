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

## The two Short examples

Run the exact smaller inputs used in the portrait mini-lessons:

```sh
python3 sorting/counting_sort/support_tickets/short_examples.py
```

**Counts become places:** Password reset (2), Payment failed (1), Update email
(2). The counts are `[1, 2]`; cumulative group ends are `[1, 3]`. Reading backward
places Update email in space 3, Payment failed in space 1, then Password reset in
space 2. These are one-based physical spaces in the visual explanation. The
function converts to zero-based indexes by decrementing before each write.

**Why read backward?** Payment failed arrives before App won't open; both have
priority 1. The group has two spaces. Reading forward while filling from space 2
would put Payment in space 2 and App in space 1, reversing arrival order. Reading
backward puts App in space 2 and Payment in space 1. This explains the pairing of
backward input traversal with decreasing group-end positions; it does not claim
that all stable Counting Sort implementations must read backward.

The Shorts and full tutorial do not yet have public video links.
