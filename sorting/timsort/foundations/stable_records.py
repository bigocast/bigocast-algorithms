"""BigOCast | Moein
Tutorial: https://bigocast.com/learn/timsort
Channel: https://www.youtube.com/@bigocast
"""

jobs = [
    {"name": "First arrival", "priority": 2},
    {"name": "Urgent request", "priority": 1},
    {"name": "Later arrival", "priority": 2},
]

ordered = sorted(jobs, key=lambda job: job["priority"])
print([job["name"] for job in ordered])
# ['Urgent request', 'First arrival', 'Later arrival']

# To change the existing list instead:
jobs.sort(key=lambda job: job["priority"])
