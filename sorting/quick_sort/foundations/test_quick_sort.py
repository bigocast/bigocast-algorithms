import itertools
import unittest

from quick_sort import partition, quicksort, quickselect


class QuickSortTests(unittest.TestCase):
    def test_exhaustive_sort_and_ranks(self):
        for size in range(7):
            for values in itertools.product((-1, 0, 1), repeat=size):
                expected = sorted(values)
                actual = list(values)
                original_id = id(actual)
                self.assertIsNone(quicksort(actual))
                self.assertEqual(actual, expected)
                self.assertEqual(id(actual), original_id)
                for k in range(1, size + 1):
                    self.assertEqual(quickselect(list(values), k), expected[k - 1])
                    self.assertEqual(quickselect(list(values), k, "largest"), expected[-k])

    def test_partition_and_subrange_contract(self):
        values = [7, 2, 9, 4, 3, 8, 5]
        self.assertEqual(partition(values, 0, 6), 3)
        self.assertEqual(values, [2, 4, 3, 5, 9, 8, 7])
        for source in itertools.product(range(3), repeat=5):
            values = [99, *source, -99]
            pivot = values[5]
            p = partition(values, 1, 5)
            self.assertEqual(values[0], 99)
            self.assertEqual(values[-1], -99)
            self.assertTrue(all(value < pivot for value in values[1:p]))
            self.assertTrue(all(value >= pivot for value in values[p + 1:6]))
            self.assertEqual(values[p], pivot)
            self.assertEqual(sorted(values[1:6]), sorted(source))
        values = [99, 3, 1, 2, -99]
        quicksort(values, 1, 3)
        self.assertEqual(values, [99, 1, 2, 3, -99])

    def test_invalid_selection(self):
        for values, rank in [([], 1), ([2], 0), ([2], 2), ([2], True), ([2], 1.5)]:
            with self.assertRaises(ValueError):
                quickselect(values, rank)
        with self.assertRaises(ValueError):
            quickselect([2], 1, "middle")


if __name__ == "__main__":
    unittest.main()
