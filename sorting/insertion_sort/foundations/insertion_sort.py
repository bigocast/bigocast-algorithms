"""BigOCast | Moein

Tutorial and interactive example: https://bigocast.com/learn/insertion-sort
YouTube channel: https://www.youtube.com/@bigocast
Visual lesson: https://youtu.be/9ufqiy4VlLI
"""

def insertion_sort(numbers):
    """Sort the original list, keeping equal values in their original order."""
    for next_index in range(1, len(numbers)):
        held = numbers[next_index]
        left = next_index - 1
        while left >= 0 and numbers[left] > held:
            numbers[left + 1] = numbers[left]
            left -= 1
        numbers[left + 1] = held
    return numbers


if __name__ == "__main__":
    numbers = [4, 7, 2, 5, 3]
    print(insertion_sort(numbers))
