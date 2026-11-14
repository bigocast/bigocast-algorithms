import itertools
import unittest
from counting_sort import counting_sort


class CountingSortTests(unittest.TestCase):
    def test_example_keeps_original_objects(self):
        cards = [(3, "A"), (1, "B"), (3, "C"), (0, "D"), (1, "E")]
        before = list(cards)
        actual = counting_sort(cards, 4)
        expected_indices = [3, 1, 4, 0, 2]
        self.assertEqual(actual, [cards[i] for i in expected_indices])
        self.assertTrue(all(x is cards[i] for x, i in zip(actual, expected_indices)))
        self.assertEqual(cards, before)

    def test_bounded_sequences_match_stable_reference(self):
        # 1,093 cases include missing keys, empty input and duplicate records.
        cases = 0
        for length in range(7):
            for keys in itertools.product([0, 1, 3], repeat=length):
                records = [(key, f"original-{i}") for i, key in enumerate(keys)]
                self.assertEqual(counting_sort(records, 4), sorted(records, key=lambda x: x[0]))
                cases += 1
        self.assertEqual(cases, 1093)

    def test_empty_zero_range(self):
        self.assertEqual(counting_sort([], 0), [])

    def test_payload_is_not_a_secondary_key(self):
        records = [(1, "Z"), (1, "A"), (0, "Q")]
        self.assertEqual(counting_sort(records, 2), [(0, "Q"), (1, "Z"), (1, "A")])


if __name__ == "__main__":
    unittest.main()
