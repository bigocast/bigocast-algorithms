"""Behavior and independent reference checks for the published shopping example."""
import unittest
from lru_cache import LRUCache, PRODUCTS, verify

class LRUCacheTests(unittest.TestCase):
    def test_reference_model_and_lesson(self):
        evidence = verify()
        self.assertEqual(evidence["oracle_operations"], 3000)
        self.assertEqual(evidence["database_reads"], 4)
        self.assertEqual(evidence["fifo_database_reads"], 5)

    def test_empty_and_zero_capacity(self):
        cache = LRUCache(0)
        self.assertIsNone(cache.get("P101"))
        cache.put("P101", PRODUCTS["P101"].copy())
        self.assertEqual(cache.order(), [])
        self.assertIsNone(cache.get("P101"))
        cache.check()

    def test_miss_does_not_touch_order(self):
        cache = LRUCache(2)
        for key in ("P101", "P202"):
            cache.put(key, PRODUCTS[key].copy())
        self.assertIsNone(cache.get("absent"))
        self.assertEqual(cache.order(), ["P101", "P202"])

    def test_records_must_be_dictionaries(self):
        with self.assertRaises(TypeError):
            LRUCache(1).put("P101", None)

if __name__ == "__main__":
    unittest.main()
