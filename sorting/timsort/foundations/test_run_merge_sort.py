import itertools
import unittest
from run_merge_sort import run_merge_sort


class SortingTests(unittest.TestCase):
    def test_outcomes_and_input_contract(self):
        cases = [[], [0], [2, 4, 7, 9, 8, 6, 1, 3, 5], list(range(20, -1, -1))]
        cases += [list(values) for size in range(6)
                  for values in itertools.product(range(3), repeat=size)]
        for values in cases:
            with self.subTest(values=values):
                original = values.copy()
                result = run_merge_sort(values)
                self.assertEqual(result, sorted(original))
                self.assertEqual(values, sorted(original) if False else original)
                self.assertEqual(result is values, False)

    def test_equal_records_keep_arrival_order(self):
        class Item:
            def __init__(self, value, label): self.value, self.label = value, label
            def __lt__(self, other): return self.value < other.value
            def __le__(self, other): return self.value <= other.value
            def __gt__(self, other): return self.value > other.value
            def __ge__(self, other): return self.value >= other.value
        items = [Item(3, 'A'), Item(2, 'B'), Item(2, 'C'), Item(1, 'D'), Item(3, 'E')]
        self.assertEqual([item.label for item in run_merge_sort(items)], ['D', 'B', 'C', 'A', 'E'])

    def test_parameters(self):
        for parameter in range(1, 17):
            values = [2, 4, 7, 9, 8, 6, 1, 3, 5]
            self.assertEqual(run_merge_sort(values, parameter), sorted(values))
        for parameter in [0, -1, 1.5, True]:
            with self.assertRaises(ValueError):
                run_merge_sort([], parameter)


if __name__ == "__main__":
    unittest.main()
