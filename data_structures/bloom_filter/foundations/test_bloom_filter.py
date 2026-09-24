"""Correctness checks for the BigOCast Bloom Filter examples, by Moein."""

from random import Random
import unittest

from bloom_filter import BloomFilter, PackedBloomFilter, sizing


class BloomFilterTests(unittest.TestCase):
    def test_exact_hash_positions_from_video(self):
        expected = {
            "dog": [9, 3, 10],
            "pig": [8, 9, 1],
            "elk": [8, 1, 7],
            "rat": [8, 10, 3],
        }
        for implementation in (BloomFilter, PackedBloomFilter):
            bloom = implementation()
            for word, positions in expected.items():
                with self.subTest(implementation=implementation.__name__, word=word):
                    self.assertEqual(list(bloom.positions(word)), positions)

    def test_exact_bit_states_from_video(self):
        bloom = BloomFilter()
        bloom.add("dog")
        self.assertEqual(bloom.bits, [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0])
        bloom.add("pig")
        self.assertEqual(bloom.bits, [0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0])

    def test_real_false_positive_and_definite_absence(self):
        inserted = {"dog", "pig"}
        self.assertNotIn("rat", inserted)
        self.assertNotIn("elk", inserted)
        for implementation in (BloomFilter, PackedBloomFilter):
            bloom = implementation()
            for word in inserted:
                bloom.add(word)
            self.assertTrue(bloom.might_contain("dog"))
            self.assertTrue(bloom.might_contain("pig"))
            self.assertFalse(bloom.might_contain("elk"))
            self.assertTrue(bloom.might_contain("rat"))

    def test_empty_filter_rejects_queries(self):
        for implementation in (BloomFilter, PackedBloomFilter):
            for m in (1, 12, 65):
                bloom = implementation(m, 3)
                for word in ("", "dog", "café", "🐕"):
                    self.assertFalse(bloom.might_contain(word))

    def test_repeated_insertions_are_idempotent(self):
        for implementation in (BloomFilter, PackedBloomFilter):
            bloom = implementation()
            bloom.add("dog")
            bloom.add("pig")
            before = bloom.bits.copy()
            for _ in range(10):
                bloom.add("dog")
            self.assertEqual(bloom.bits, before)

    def test_no_false_negatives_and_packed_equivalence(self):
        rng = Random(240926)
        words = ["", "dog", "pig", "café", "🐕", "مرحبا"]
        words.extend(f"key-{rng.getrandbits(64)}" for _ in range(200))
        missing = [f"missing-{index}" for index in range(200)]
        for m in (1, 7, 8, 9, 12, 64, 65, 4096):
            for k in (1, 3, 5):
                with self.subTest(m=m, k=k):
                    readable = BloomFilter(m, k)
                    packed = PackedBloomFilter(m, k)
                    for word in words:
                        readable.add(word)
                        packed.add(word)
                    for word in words:
                        self.assertTrue(readable.might_contain(word))
                        self.assertTrue(packed.might_contain(word))
                    for word in words + missing:
                        self.assertEqual(readable.might_contain(word), packed.might_contain(word))
                    self.assertEqual(len(packed.bits), (m + 7) // 8)
                    for position in range(m):
                        self.assertEqual(
                            readable.bits[position],
                            (packed.bits[position // 8] >> (position % 8)) & 1,
                        )
                    if m % 8:
                        self.assertEqual(packed.bits[-1] >> (m % 8), 0)

    def test_saturated_filter_can_match_everything(self):
        for implementation in (BloomFilter, PackedBloomFilter):
            bloom = implementation(1, 3)
            bloom.add("dog")
            self.assertTrue(bloom.might_contain("never inserted"))

    def test_unsafe_deletion_reproduces_the_short(self):
        bloom = BloomFilter()
        bloom.add("dog")
        bloom.add("pig")
        self.assertTrue(bloom.might_contain("dog"))
        for position in bloom.positions("pig"):
            bloom.bits[position] = 0
        self.assertFalse(bloom.might_contain("dog"))

    def test_sizing_example_from_video(self):
        m, k = sizing(1_000_000, 0.01)
        self.assertEqual((m, k), (9_585_059, 7))
        self.assertEqual((m + 7) // 8, 1_198_133)
        self.assertEqual(sizing(1, 0.99), (1, 1))

    def test_invalid_filter_parameters(self):
        for implementation in (BloomFilter, PackedBloomFilter):
            for value in (0, -1, 1.5, True, False, "12", None):
                with self.subTest(implementation=implementation.__name__, value=value):
                    with self.assertRaises(ValueError):
                        implementation(value, 3)
                    with self.assertRaises(ValueError):
                        implementation(12, value)

    def test_invalid_sizing_parameters(self):
        for n in (0, -1, True, 1.5):
            with self.assertRaises(ValueError):
                sizing(n, 0.01)
        for p in (0, 1, -0.1, 1.1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                sizing(100, p)


if __name__ == "__main__":
    unittest.main()
