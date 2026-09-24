"""BigOCast | Moein: reproduce the Bloom Filter deletion Short's deliberate bug.

Clearing an item's bits is unsafe. This is a failure demonstration, not a deletion
API. The ordinary BloomFilter implementation supports only add and might_contain.
"""

from bloom_filter import BloomFilter


if __name__ == "__main__":
    bloom = BloomFilter()
    bloom.add("dog")
    bloom.add("pig")
    print("Inserted dog and pig; both use bit 9.")
    print("Before clearing pig's bits, dog:", bloom.might_contain("dog"))

    # Intentionally wrong: these positions can also belong to another item.
    for position in bloom.positions("pig"):
        bloom.bits[position] = 0

    print("After clearing pig's bits, dog:", bloom.might_contain("dog"))
    print("False negative: dog was never removed. Do not delete by clearing bits.")
