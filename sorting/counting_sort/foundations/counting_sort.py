"""Stable Counting Sort for (integer key, payload) records.

BigOCast | Moein

Tutorial and visualiser: https://bigocast.com/learn/counting-sort
YouTube channel: https://www.youtube.com/@bigocast
A matching public video has not been released yet.

Precondition: K is a nonnegative integer and every key is in range(K).
The payload is carried unchanged; it is never used as a secondary sort key.
"""


def counting_sort(items, K):
    """Return the original records ordered stably by key, without changing items."""
    counts = [0] * K
    for key, _ in items:
        counts[key] += 1

    for key in range(1, K):
        counts[key] += counts[key - 1]

    output = [None] * len(items)
    for item in reversed(items):
        key = item[0]
        counts[key] -= 1
        output[counts[key]] = item

    return output


if __name__ == "__main__":
    cards = [(3, "A"), (1, "B"), (3, "C"), (0, "D"), (1, "E")]
    print(counting_sort(cards, K=4))
