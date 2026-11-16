"""BigOCast | Moein

Tutorial and interactive example: https://bigocast.com/learn/heap-sort
YouTube channel: https://www.youtube.com/@bigocast
Visual lesson: https://youtu.be/jtshKZDqeYo
"""

def heap_sort(numbers):
    """Sort the original list using a max-heap and iterative sift-down."""
    def sift_down(root, end):
        while 2 * root + 1 <= end:
            left = 2 * root + 1
            right = left + 1
            largest = root
            if numbers[left] > numbers[largest]:
                largest = left
            if right <= end and numbers[right] > numbers[largest]:
                largest = right
            if largest == root:
                return
            numbers[root], numbers[largest] = numbers[largest], numbers[root]
            root = largest

    for root in range(len(numbers) // 2 - 1, -1, -1):
        sift_down(root, len(numbers) - 1)
    for end in range(len(numbers) - 1, 0, -1):
        numbers[0], numbers[end] = numbers[end], numbers[0]
        sift_down(0, end - 1)
    return numbers


if __name__ == "__main__":
    numbers = [4, 7, 2, 9, 1, 5]
    print(heap_sort(numbers))
