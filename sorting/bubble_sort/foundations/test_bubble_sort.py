"""Behaviour checks for the BigOCast Bubble Sort lesson."""

from itertools import product
import unittest

from bubble_sort import bubble_sort


class Item:
    comparisons = 0

    def __init__(self, value, identity):
        self.value = value
        self.identity = identity

    def __gt__(self, other):
        type(self).comparisons += 1
        return self.value > other.value


class BubbleSortTests(unittest.TestCase):
    def test_values_and_in_place_return_for_small_inputs(self):
        for length in range(6):
            for values in product((-1, 0, 1), repeat=length):
                for early in (True, False):
                    numbers = list(values)
                    self.assertIs(bubble_sort(numbers, early), numbers)
                    self.assertEqual(numbers, sorted(values))

    def test_stability_preserves_equal_item_identity(self):
        for early in (True, False):
            numbers = [Item(3, "3a"), Item(1, "1a"), Item(3, "3b"), Item(2, "2"), Item(1, "1b")]
            original = numbers.copy()
            bubble_sort(numbers, early)
            self.assertEqual([item.identity for item in numbers], ["1a", "1b", "2", "3a", "3b"])
            self.assertEqual({id(item) for item in numbers}, {id(item) for item in original})

    def test_comparison_counts_match_the_lesson(self):
        cases = [([1, 2, 3, 4, 5], True, 4),
                 ([1, 2, 3, 4, 5], False, 10),
                 ([2, 3, 4, 5, 1], True, 10),
                 ([5, 1, 4, 2, 3], True, 9)]
        for values, early, expected in cases:
            numbers = [Item(value, index) for index, value in enumerate(values)]
            Item.comparisons = 0
            bubble_sort(numbers, early)
            self.assertEqual(Item.comparisons, expected)
            self.assertEqual([item.value for item in numbers], sorted(values))


if __name__ == "__main__":
    unittest.main()
