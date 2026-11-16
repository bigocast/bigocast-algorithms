"""BigOCast | Moein

Tutorial and interactive example: https://bigocast.com/learn/gnome-sort
YouTube channel: https://www.youtube.com/@bigocast
Visual lesson: https://youtu.be/9cIjvXEeOhQ
"""

def gnome_sort(numbers):
    """Sort in place by walking forward or swapping and stepping back."""
    cursor = 0
    while cursor < len(numbers):
        if cursor == 0 or numbers[cursor - 1] <= numbers[cursor]:
            cursor += 1
        else:
            numbers[cursor - 1], numbers[cursor] = (
                numbers[cursor], numbers[cursor - 1]
            )
            cursor -= 1
    return numbers


if __name__ == "__main__":
    numbers = [4, 2, 3, 1]
    print(gnome_sort(numbers))
