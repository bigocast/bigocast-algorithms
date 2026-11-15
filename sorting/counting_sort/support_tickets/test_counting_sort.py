"""Behavioral checks for the lesson's whole-ticket stable sort."""
import itertools
import unittest

from counting_sort import counting_sort


class CountingSortTests(unittest.TestCase):
    def test_lesson_example_keeps_the_original_tickets(self):
        tickets = [
            {"subject": subject, "priority": priority}
            for subject, priority in [
                ("Password reset", 2), ("Payment failed", 1),
                ("Change photo", 3), ("App won't open", 1),
                ("Update email", 2),
            ]
        ]
        snapshot = [dict(ticket) for ticket in tickets]
        result = counting_sort(tickets, 3)
        self.assertEqual([t["subject"] for t in result], [
            "Payment failed", "App won't open", "Password reset",
            "Update email", "Change photo",
        ])
        for actual, index in zip(result, [1, 3, 0, 4, 2]):
            self.assertIs(actual, tickets[index])
        self.assertEqual(tickets, snapshot)

    def test_all_short_priority_sequences_against_stable_reference(self):
        for length in range(8):
            for priorities in itertools.product(range(1, 4), repeat=length):
                tickets = [{"priority": p, "arrival": i} for i, p in enumerate(priorities)]
                expected = sorted(tickets, key=lambda t: t["priority"])
                actual = counting_sort(tickets, 3)
                self.assertEqual(actual, expected)
                self.assertTrue(all(a is b for a, b in zip(actual, expected)))

    def test_unused_priorities_do_not_change_the_result(self):
        tickets = [{"priority": 4, "subject": "Z"}, {"priority": 1, "subject": "Q"}, {"priority": 4, "subject": "A"}]
        self.assertEqual(counting_sort(tickets, 8), [tickets[1], tickets[0], tickets[2]])

    def test_counts_short_keeps_the_normal_requests_in_arrival_order(self):
        from short_examples import COUNTS_EXAMPLE
        result = counting_sort(COUNTS_EXAMPLE, 2)
        self.assertEqual([t["subject"] for t in result], [
            "Payment failed", "Password reset", "Update email",
        ])
        self.assertIs(result[1], COUNTS_EXAMPLE[0])
        self.assertIs(result[2], COUNTS_EXAMPLE[2])

    def test_stability_short_keeps_the_earlier_urgent_request_first(self):
        from short_examples import STABILITY_EXAMPLE
        result = counting_sort(STABILITY_EXAMPLE, 1)
        self.assertIs(result[0], STABILITY_EXAMPLE[0])
        self.assertIs(result[1], STABILITY_EXAMPLE[1])

    def test_empty_input(self):
        self.assertEqual(counting_sort([], 0), [])
        self.assertEqual(counting_sort([], 3), [])


if __name__ == "__main__":
    unittest.main()
