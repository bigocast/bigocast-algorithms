"""Bubble Sort with shrinking passes and optional early stopping.

BigOCast | Moein

Tutorial and visualiser: https://bigocast.com/learn/bubble-sort
Video: https://www.youtube.com/watch?v=MadYeOwpZBY
YouTube channel: https://www.youtube.com/@bigocast

Sort a mutable list of mutually comparable values in ascending order.
The list is changed in place and returned. Equal items keep their original order.
"""


def bubble_sort(numbers, stop_early=True):
    """Sort the original list from smallest to largest and return it."""
    for end in range(len(numbers) - 1, 0, -1):
        swapped = False

        for left in range(end):
            right = left + 1
            if numbers[left] > numbers[right]:
                numbers[left], numbers[right] = numbers[right], numbers[left]
                swapped = True

        if stop_early and not swapped:
            break

    return numbers


if __name__ == "__main__":
    numbers = [5, 1, 4, 2, 3]
    print(bubble_sort(numbers))
    # [1, 2, 3, 4, 5]
