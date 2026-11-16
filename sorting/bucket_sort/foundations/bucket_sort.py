"""BigOCast | Moein

Tutorial and interactive example: https://bigocast.com/learn/radix-sort
YouTube channel: https://www.youtube.com/@bigocast
No matching video is published for this example yet.
"""

def bucket_sort(numbers, bucket_count=5):
    """Return a stable sorted copy of integers from 0 through 99."""
    if type(bucket_count) is not int or bucket_count < 1:
        raise ValueError("bucket_count must be a positive integer")
    if any(type(value) is not int or not 0 <= value < 100 for value in numbers):
        raise ValueError("use integers from 0 through 99")
    buckets = [[] for _ in range(bucket_count)]
    for value in numbers:
        buckets[value * bucket_count // 100].append(value)
    for bucket in buckets:
        for i in range(1, len(bucket)):
            held = bucket[i]
            left = i - 1
            while left >= 0 and bucket[left] > held:
                bucket[left + 1] = bucket[left]
                left -= 1
            bucket[left + 1] = held
    return [value for bucket in buckets for value in bucket]


if __name__ == "__main__":
    numbers = [42, 7, 76, 31, 95, 12]
    print(bucket_sort(numbers))
