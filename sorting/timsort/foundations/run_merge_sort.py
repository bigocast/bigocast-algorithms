"""BigOCast | Moein

Tutorial and interactive example: https://bigocast.com/learn/timsort
YouTube channel: https://www.youtube.com/@bigocast
No matching video is published for this example yet.
"""

def run_merge_sort(numbers, minrun=3):
    """Teaching model, NOT full Timsort: natural runs + binary insertion + merges.

    Returns a new list. Uses pairwise merge rounds, not Powersort or TimSort's
    stack policy, and does not implement galloping. Strict descending runs
    keep reversal stable. The tiny minrun is for the interactive lesson.
    """
    if type(minrun) is not int or minrun < 1:
        raise ValueError("minrun must be a positive integer")
    result = list(numbers)
    runs = []
    start = 0
    while start < len(result):
        end = start + 1
        descending = end < len(result) and result[end] < result[start]
        if end < len(result):
            end += 1
        while end < len(result):
            if descending:
                if result[end] >= result[end - 1]:
                    break
            elif result[end] < result[end - 1]:
                break
            end += 1
        if descending:
            result[start:end] = reversed(result[start:end])
        target = min(len(result), max(end, start + minrun))
        for i in range(end, target):
            held = result[i]
            low, high = start, i
            while low < high:
                middle = (low + high) // 2
                if held < result[middle]:
                    high = middle
                else:
                    low = middle + 1
            for j in range(i, low, -1):
                result[j] = result[j - 1]
            result[low] = held
        runs.append((start, target))
        start = target

    while len(runs) > 1:
        next_runs = []
        for r in range(0, len(runs), 2):
            if r + 1 == len(runs):
                next_runs.append(runs[r])
                continue
            start, middle = runs[r]
            _, end = runs[r + 1]
            left, right = result[start:middle], result[middle:end]
            merged = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
            merged.extend(left[i:])
            merged.extend(right[j:])
            result[start:end] = merged
            next_runs.append((start, end))
        runs = next_runs
    return result


if __name__ == "__main__":
    numbers = [2, 4, 7, 9, 8, 6, 1, 3, 5]
    print(run_merge_sort(numbers))
