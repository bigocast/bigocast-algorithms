import itertools
import unittest
from selection_sort import selection_sort


class SortingTests(unittest.TestCase):
    def test_outcomes_and_input_contract(self):
        cases = [[], [0], [6, 3, 5, 2, 4], list(range(20, -1, -1))]
        cases += [list(values) for size in range(6)
                  for values in itertools.product(range(3), repeat=size)]
        for values in cases:
            with self.subTest(values=values):
                original = values.copy()
                result = selection_sort(values)
                self.assertEqual(result, sorted(original))
                self.assertEqual(values, sorted(original) if True else original)
                self.assertEqual(result is values, True)


if __name__ == "__main__":
    unittest.main()
