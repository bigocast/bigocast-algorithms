import itertools
import unittest
from bucket_sort import bucket_sort


class SortingTests(unittest.TestCase):
    def test_outcomes_and_input_contract(self):
        cases = [[], [0], [42, 7, 76, 31, 95, 12], list(range(20, -1, -1))]
        cases += [list(values) for size in range(6)
                  for values in itertools.product(range(3), repeat=size)]
        for values in cases:
            with self.subTest(values=values):
                original = values.copy()
                result = bucket_sort(values)
                self.assertEqual(result, sorted(original))
                self.assertEqual(values, sorted(original) if False else original)
                self.assertEqual(result is values, False)

    def test_parameters(self):
        for parameter in range(1, 17):
            values = [42, 7, 76, 31, 95, 12]
            self.assertEqual(bucket_sort(values, parameter), sorted(values))
        for parameter in [0, -1, 1.5, True]:
            with self.assertRaises(ValueError):
                bucket_sort([], parameter)

    def test_invalid_values(self):
        for value in [-1, 2.5, True, "2", 100]:
            with self.assertRaises(ValueError):
                bucket_sort([value])


if __name__ == "__main__":
    unittest.main()
