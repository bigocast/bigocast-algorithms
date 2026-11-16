"""BigOCast | Moein

Tutorial and interactive example: https://bigocast.com/learn/selection-sort
YouTube channel: https://www.youtube.com/@bigocast
Visual lesson: https://youtu.be/2LddD0KCIzY
"""

def selection_sort(numbers):
    """Sort the original list and return that same list."""
    for start in range(len(numbers) - 1):
        minimum = start
        for scan in range(start + 1, len(numbers)):
            if numbers[scan] < numbers[minimum]:
                minimum = scan
        if minimum != start:
            numbers[start], numbers[minimum] = numbers[minimum], numbers[start]
    return numbers


if __name__ == "__main__":
    numbers = [6, 3, 5, 2, 4]
    print(selection_sort(numbers))
