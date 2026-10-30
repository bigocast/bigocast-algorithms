"""Independent full-sort oracle and stream contract. BigOCast | Moein."""
import random
import unittest
from collections import Counter

from largest_files import FILES, largest_files


class LargestFilesTests(unittest.TestCase):
    def test_video_result(self):
        self.assertEqual(largest_files(iter(FILES)), [
            (150, "project.mov"), (140, "backup.zip"), (120, "archive.zip")])

    def test_empty_and_capacity_larger_than_input(self):
        self.assertEqual(largest_files([], 3), [])
        self.assertEqual(largest_files(iter(FILES), 20), sorted(FILES, reverse=True))

    def test_zero_does_not_consume_input(self):
        def unreadable():
            raise AssertionError("zero capacity must not read the input")
            yield
        self.assertEqual(largest_files(unreadable(), 0), [])

    def test_negative_capacity(self):
        with self.assertRaises(ValueError):
            largest_files(FILES, -1)

    def test_equal_cutoff_does_not_replace(self):
        self.assertEqual(largest_files([(7, "a"), (7, "b")], 1), [(7, "a")])

    def test_against_independent_sort_with_duplicates(self):
        rng = random.Random(73174)
        for n in range(50):
            records = [(rng.randrange(20), f"file-{i}") for i in range(n)]
            original = list(records)
            for k in (0, 1, 2, 3, 7, 60):
                with self.subTest(n=n, k=k):
                    result = largest_files(iter(records), k)
                    self.assertEqual([size for size, _ in result],
                                     sorted((size for size, _ in records), reverse=True)[:k])
                    self.assertFalse(Counter(result) - Counter(records))
                    self.assertEqual(records, original)


if __name__ == "__main__":
    unittest.main()
