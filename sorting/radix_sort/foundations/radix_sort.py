"""BigOCast | Moein

Tutorial and interactive example: https://bigocast.com/learn/radix-sort
YouTube channel: https://www.youtube.com/@bigocast
No matching video is published for this example yet.
"""

def radix_sort(numbers, base=10):
    """Return a stable sorted copy of nonnegative integers."""
    if type(base) is not int or base < 2:
        raise ValueError("base must be an integer of at least 2")
    if any(type(value) is not int or value < 0 for value in numbers):
        raise ValueError("use nonnegative integers")
    result = list(numbers)
    place = 1
    maximum = max(result, default=0)
    while maximum // place > 0:
        buckets = [[] for _ in range(base)]
        for value in result:
            digit = (value // place) % base
            buckets[digit].append(value)
        result = [value for bucket in buckets for value in bucket]
        place *= base
    return result


if __name__ == "__main__":
    numbers = [42, 17, 24, 12, 7, 31]
    print(radix_sort(numbers))
