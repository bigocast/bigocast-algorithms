import itertools
import unittest
from heap_sort import heap_sort


class SortingTests(unittest.TestCase):
    def test_outcomes_and_input_contract(self):
        cases = [[], [0], [4, 7, 2, 9, 1, 5], list(range(20, -1, -1))]
        cases += [list(values) for size in range(6)
                  for values in itertools.product(range(3), repeat=size)]
        for values in cases:
            with self.subTest(values=values):
                original = values.copy()
                result = heap_sort(values)
                self.assertEqual(result, sorted(original))
                self.assertEqual(values, sorted(original) if True else original)
                self.assertEqual(result is values, True)


if __name__ == "__main__":
    unittest.main()
