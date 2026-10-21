"""BigOCast | Moein: executable checks for the complete three-slot lesson."""
import unittest
from lru_cache import LRUCache, PRODUCTS, implementation_walkthrough, verify

class CacheTests(unittest.TestCase):
    def test_demonstrations_and_independent_oracle(self):
        result = verify()
        self.assertEqual(result['database_reads'], 4)
        self.assertEqual(result['fifo_database_reads'], 5)
        self.assertEqual(result['oracle_operations'], 3000)
        self.assertEqual(result['no_hit_workload_reads'], 12)

    def test_code_walkthrough_states(self):
        self.assertEqual(implementation_walkthrough(), {
            'request_trace_end': ['P202','P404','P101'],
            'structures_end': ['P202','P101','P404'],
            'helpers_end': ['P202','P404','P101'],
            'get_end': ['P202','P101','P404'],
            'update_end': ['P101','P404','P202'],
            'insert_end': ['P404','P202','P303'],
        })

    def test_eviction_happens_before_insertion(self):
        class ObservedCache(LRUCache):
            def _append(self, node):
                assert len(self.nodes) <= self.capacity
                super()._append(node)
        for capacity in (0, 1, 3):
            cache = ObservedCache(capacity)
            for key, value in PRODUCTS.items():
                cache.put(key, value.copy())
                cache.check()

    def test_update_and_miss_preserve_contract(self):
        cache = LRUCache(1)
        cache.put('P101', PRODUCTS['P101'].copy())
        node = cache.nodes['P101']
        value = {'category': 'Wireless'}
        cache.put('P101', value)
        self.assertIs(cache.nodes['P101'], node)
        self.assertIs(cache.get('P101'), value)
        self.assertIsNone(cache.get('P202'))
        self.assertEqual(cache.order(), ['P101'])
        with self.assertRaises(TypeError):
            cache.put('P202', None)
        cache.check()

if __name__ == '__main__':
    unittest.main()
