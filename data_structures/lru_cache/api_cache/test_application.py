"""BigOCast | Moein. Check actual SQLite work and the local HTTP service."""
import unittest
import http.client
import queue
import re
import subprocess
import sys
import threading
from pathlib import Path
from api_cache import ProductStore, ProductAPI, PRODUCTS, request_trace, CYCLE_REQUESTS


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.store = ProductStore()
        self.api = ProductAPI(self.store, 3)

    def tearDown(self):
        self.store.close()

    def test_repeated_route_returns_same_record_with_one_executed_select(self):
        first = self.api.handle_get('/products/42')
        second = self.api.handle_get('/products/42')
        self.assertEqual(first, second)
        self.assertEqual(first, (200, PRODUCTS[42]._asdict()))
        self.assertEqual(len(self.store.selects), 1)
        self.assertIn('WHERE id = 42', self.store.selects[0])
        second[1]['name'] = 'caller mutation'
        self.assertEqual(self.api.get_product(42).name, 'Keyboard')

    def test_uncached_calls_really_execute_twice(self):
        self.assertEqual(self.store.fetch(42), self.store.fetch(42))
        self.assertEqual(len(self.store.selects), 2)

    def test_evicted_record_remains_in_database(self):
        for key in (42, 17, 83, 42, 91):
            self.api.handle_get(f'/products/{key}')
        self.assertNotIn(17, self.api.cache.nodes)
        self.assertEqual(self.store.fetch(17), PRODUCTS[17])
        self.assertEqual(len(self.store.selects), 5)

    def test_invalid_routes_do_not_query_or_pollute_cache(self):
        for path in ('/', '/products/', '/products/-1', '/products/42?currency=GBP',
                     '/products/42/extra', '/products/１２', '/products/' + '9' * 5000):
            self.assertEqual(self.api.handle_get(path)[0], 404)
        self.assertEqual(self.store.selects, [])
        self.assertEqual(self.api.cache.items(), [])

    def test_not_found_does_not_evict_valid_entries(self):
        for key in (42, 17, 83):
            self.api.get_product(key)
        before = self.api.cache.items()
        self.assertEqual(self.api.handle_get('/products/999')[0], 404)
        self.assertEqual(self.api.cache.items(), before)
        self.assertEqual(len(self.store.selects), 4)

    def test_storage_failure_leaves_cache_intact(self):
        for key in (42, 17, 83):
            self.api.get_product(key)
        before = self.api.cache.items()
        def fail(key):
            raise RuntimeError('database unavailable')
        self.store.fetch = fail
        with self.assertRaises(RuntimeError):
            self.api.get_product(91)
        self.assertEqual(self.api.cache.items(), before)

    def test_trace_rejects_non_integer_or_unknown_product_ids(self):
        for value in (42.0, [], '42', True, None, 999):
            with self.subTest(value=value), self.assertRaises(ValueError):
                request_trace((value,))

    def test_http_cli_announces_bound_port_and_preserves_cache_between_requests(self):
        script = Path(__file__).with_name('api_cache.py')
        process = subprocess.Popen(
            [sys.executable, '-B', str(script), '--serve', '--port', '0'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        try:
            ready = queue.Queue()
            threading.Thread(target=lambda: ready.put(process.stdout.readline()), daemon=True).start()
            startup = ready.get(timeout=5).strip()
            match = re.fullmatch(r'Read-only demo: http://127\.0\.0\.1:(\d+)/products/42', startup)
            self.assertIsNotNone(match, startup)
            port = int(match.group(1))
            self.assertGreater(port, 0)
            self.assertLessEqual(port, 65535)
            for path, status, queries in (
                ('/products/42', 200, 1), ('/products/42', 200, 1),
                ('/products/17', 200, 2), ('/products/83', 200, 3),
                ('/products/42', 200, 3), ('/products/91', 200, 4),
                ('/products/42', 200, 4), ('/products/17', 200, 5),
                ('/products/999', 404, 6), ('/products/17', 200, 6),
                ('/products/42?currency=GBP', 404, 6),
            ):
                with self.subTest(path=path, queries=queries):
                    connection = http.client.HTTPConnection('127.0.0.1', port, timeout=5)
                    try:
                        connection.request('GET', path)
                        response = connection.getresponse()
                        body = response.read()
                        self.assertEqual(response.status, status)
                        self.assertEqual(int(response.getheader('X-Database-Queries')), queries)
                        self.assertEqual(int(response.getheader('Content-Length')), len(body))
                        self.assertEqual(response.getheader('Content-Type'), 'application/json; charset=utf-8')
                    finally:
                        connection.close()
            self.assertIsNone(process.poll())
        finally:
            process.terminate()
            try:
                process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate(timeout=5)

    def test_all_misses_counts_executed_queries(self):
        small = request_trace(CYCLE_REQUESTS, 3)
        large = request_trace(CYCLE_REQUESTS, 4)
        self.assertEqual([s['queries'] for s in small['steps']], list(range(1, 9)))
        self.assertEqual([s['queries'] for s in large['steps']], [1, 2, 3, 4, 4, 4, 4, 4])
        self.assertTrue(all(s['sql'] is None for s in large['steps'][4:]))


if __name__ == '__main__':
    unittest.main()
