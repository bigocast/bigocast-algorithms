import itertools
import unittest
from gnome_sort import gnome_sort


class SortingTests(unittest.TestCase):
    def test_outcomes_and_input_contract(self):
        cases = [[], [0], [4, 2, 3, 1], list(range(20, -1, -1))]
        cases += [list(values) for size in range(6)
                  for values in itertools.product(range(3), repeat=size)]
        for values in cases:
            with self.subTest(values=values):
                original = values.copy()
                result = gnome_sort(values)
                self.assertEqual(result, sorted(original))
                self.assertEqual(values, sorted(original) if True else original)
                self.assertEqual(result is values, True)

    def test_equal_records_keep_arrival_order(self):
        class Item:
            def __init__(self, value, label): self.value, self.label = value, label
            def __lt__(self, other): return self.value < other.value
            def __le__(self, other): return self.value <= other.value
            def __gt__(self, other): return self.value > other.value
            def __ge__(self, other): return self.value >= other.value
        items = [Item(3, 'A'), Item(2, 'B'), Item(2, 'C'), Item(1, 'D'), Item(3, 'E')]
        self.assertEqual([item.label for item in gnome_sort(items)], ['D', 'B', 'C', 'A', 'E'])


if __name__ == "__main__":
    unittest.main()
