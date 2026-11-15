"""The exact smaller examples in BigOCast's two Counting Sort Shorts.

Both call the complete stable algorithm used by the full lesson.
"""
from counting_sort import counting_sort

COUNTS_EXAMPLE = [
    {"subject": "Password reset", "priority": 2},
    {"subject": "Payment failed", "priority": 1},
    {"subject": "Update email", "priority": 2},
]

STABILITY_EXAMPLE = [
    {"subject": "Payment failed", "priority": 1},
    {"subject": "App won't open", "priority": 1},
]


if __name__ == "__main__":
    for label, tickets, levels in [
        ("Counts become places", COUNTS_EXAMPLE, 2),
        ("Keep equal priorities in arrival order", STABILITY_EXAMPLE, 1),
    ]:
        print(label)
        for ticket in counting_sort(tickets, levels):
            print(ticket["priority"], ticket["subject"])
        print()
