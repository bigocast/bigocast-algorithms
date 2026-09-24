"""Bloom filters: definitely absent or possibly present.

BigOCast | Moein
Companion to "Bloom Filters Explained: Skip Database Reads with a Few Bits".
The list version favors readable code; the packed version uses actual bit storage.
Both use the exact deterministic hash procedure taught in the video.
"""

from collections.abc import Iterator
from hashlib import sha256
from math import ceil, log


class BloomFilter:
    bits: list[int] | bytearray

    def __init__(self, m: int = 12, k: int = 3) -> None:
        if type(m) is not int or type(k) is not int or m <= 0 or k <= 0:
            raise ValueError("m and k must be positive integers")
        self.m = m
        self.k = k
        self.bits = [0] * m

    def positions(self, item: str) -> Iterator[int]:
        for seed in range(self.k):
            data = f"{seed}:{item}".encode()
            digest = sha256(data).digest()
            number = int.from_bytes(digest[:8], "big")
            yield number % self.m

    def add(self, item: str) -> None:
        for index in self.positions(item):
            self.bits[index] = 1

    def might_contain(self, item: str) -> bool:
        for index in self.positions(item):
            if self.bits[index] == 0:
                return False
        return True


class PackedBloomFilter(BloomFilter):
    """Same logical bit array, stored in ceil(m / 8) bytes (plus Python overhead)."""

    def __init__(self, m: int = 12, k: int = 3) -> None:
        if type(m) is not int or type(k) is not int or m <= 0 or k <= 0:
            raise ValueError("m and k must be positive integers")
        self.m, self.k = m, k
        self.bits = bytearray((m + 7) // 8)

    def add(self, item: str) -> None:
        for index in self.positions(item):
            self.bits[index // 8] |= 1 << (index % 8)

    def might_contain(self, item: str) -> bool:
        for index in self.positions(item):
            if not self.bits[index // 8] & (1 << (index % 8)):
                return False
        return True


def sizing(n: int, p: float) -> tuple[int, int]:
    """Usual large-filter approximation; choose capacity before inserting items."""
    if type(n) is not int or n <= 0 or not 0 < p < 1:
        raise ValueError("n must be positive and p must be between zero and one")
    m = ceil(-n * log(p) / log(2) ** 2)
    return m, max(1, round(m / n * log(2)))


if __name__ == "__main__":
    bloom = BloomFilter()
    inserted = {"dog", "pig"}
    for word in ("dog", "pig"):
        print(f"{word} positions: {list(bloom.positions(word))}")
        bloom.add(word)
        print(f"After {word}: {bloom.bits}")
    print()
    for word in ("dog", "pig", "elk", "rat"):
        answer = "possibly present" if bloom.might_contain(word) else "definitely absent"
        actual = "inserted" if word in inserted else "not inserted"
        print(f"{word}: {answer} ({actual})")
    m, k = sizing(1_000_000, 0.01)
    print(f"\nSizing example: {m:,} bits, {k} hashes")
    print(f"Packed array: {(m + 7) // 8:,} bytes before Python overhead")
