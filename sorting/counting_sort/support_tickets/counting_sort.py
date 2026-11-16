"""Stable Counting Sort for the BigOCast support-ticket lesson, by Moein.

Tutorial and adjustable visualiser: https://bigocast.com/learn/counting-sort
Video: https://youtu.be/EdQHMAcq0yc
Scheduled for 23 November 2026, 10:00 UK time.
YouTube channel: https://www.youtube.com/@bigocast

Precondition: levels is a nonnegative integer. Each ticket has an integer
priority between 1 and levels. No validation is included in the teaching code.
"""


def counting_sort(tickets, levels):
    counts = [0] * levels

    for ticket in tickets:
        p = ticket["priority"] - 1
        counts[p] += 1

    for p in range(1, levels):
        counts[p] += counts[p - 1]

    result = [None] * len(tickets)
    for ticket in reversed(tickets):
        p = ticket["priority"] - 1
        counts[p] -= 1
        result[counts[p]] = ticket

    return result


if __name__ == "__main__":
    tickets = [
        {"subject": "Password reset", "priority": 2},
        {"subject": "Payment failed", "priority": 1},
        {"subject": "Change photo", "priority": 3},
        {"subject": "App won't open", "priority": 1},
        {"subject": "Update email", "priority": 2},
    ]
    for ticket in counting_sort(tickets, levels=3):
        print(ticket["priority"], ticket["subject"])
