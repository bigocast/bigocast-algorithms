"""BigOCast | Moein

Tutorial and interactive example: https://bigocast.com/learn/merge-sort
YouTube channel: https://www.youtube.com/@bigocast
Visual lesson: https://youtu.be/gxdZubPijxQ
"""

def merge_sort(numbers):
    """Return a new sorted list; leave the original list unchanged."""
    if len(numbers) <= 1:
        return numbers.copy()

    middle = len(numbers) // 2
    left = merge_sort(numbers[:middle])
    right = merge_sort(numbers[middle:])
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


if __name__ == "__main__":
    numbers = [7, 2, 5, 1, 6, 3]
    print(merge_sort(numbers))
