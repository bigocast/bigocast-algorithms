"""Top K file sizes in one pass. BigOCast | Moein."""

from heapq import heappush, heapreplace


def largest_files(files, k=3):
    """Return up to k records, largest first."""
    if k < 0:
        raise ValueError("k must be nonnegative")
    if k == 0:
        return []
    heap = []
    for size, name in files:
        entry = (size, name)
        if len(heap) < k:
            heappush(heap, entry)
        elif size > heap[0][0]:
            heapreplace(heap, entry)
    return sorted(heap, reverse=True)


FILES = [
    (80, "interview.mov"),
    (30, "notes.pdf"),
    (120, "archive.zip"),
    (90, "dataset.csv"),
    (10, "debug.log"),
    (140, "backup.zip"),
    (60, "preview.mp4"),
    (110, "sessions.bin"),
    (150, "project.mov"),
    (40, "readme.txt"),
]


if __name__ == "__main__":
    for size, name in largest_files(iter(FILES), 3):
        print(f"{name}: {size} MB")
