# BigOCast algorithms

Complete Python examples from BigOCast, by Moein. Run the algorithms, change the
inputs, and follow the same decisions explained in the videos.

## Browse the lessons

| Category | Lesson | What you can try |
| --- | --- | --- |
| Sorting | [Selection Sort](sorting/selection_sort/foundations/) | Run the lesson example and verify it against exhaustive small inputs. |
| Sorting | [Insertion Sort](sorting/insertion_sort/foundations/) | Run the lesson example and verify it against exhaustive small inputs. |
| Sorting | [Gnome Sort](sorting/gnome_sort/foundations/) | Run the lesson example and verify it against exhaustive small inputs. |
| Sorting | [Merge Sort](sorting/merge_sort/foundations/) | Run the lesson example and verify it against exhaustive small inputs. |
| Sorting | [Heap Sort](sorting/heap_sort/foundations/) | Run the lesson example and verify it against exhaustive small inputs. |
| Sorting | [Radix Sort](sorting/radix_sort/foundations/) | Run the lesson example and verify it against exhaustive small inputs. |
| Sorting | [Bucket Sort](sorting/bucket_sort/foundations/) | Run the lesson example and verify it against exhaustive small inputs. |
| Sorting | [Timsort ideas](sorting/timsort/foundations/) | Run the lesson example and verify it against exhaustive small inputs. |
| Sorting | [Quick Sort and Quickselect](sorting/quick_sort/foundations/) | Partition one array, follow recursive sorting, and find a rank with duplicates. |
| Sorting | [Bubble Sort](sorting/bubble_sort/foundations/) | Follow the largest value through a pass, compare early stopping, and test equal values and empty input. |
| Sorting | [Counting Sort: support tickets](sorting/counting_sort/support_tickets/) | Sort whole requests by priority while keeping equal priorities in arrival order; reproduce the video example and test stability. |
| Sorting | [Counting Sort](sorting/counting_sort/foundations/) | Keep original labelled cards through counting, prefix sums and stable placement; test duplicates, missing keys and empty input. |
| Graph search | [Dijkstra delivery route](graphs/dijkstra/delivery/) | Solve the five-place delivery map, then test ties, zero-cost cycles, unreachable goals, and the nonnegative contract. |
| Graph search | [A* foundations](graphs/a_star/foundations/) | Find a shortest route around a wall, then try an open floor. |
| Graph search | [A* sliding puzzle](graphs/a_star/sliding_puzzle/) | Solve the classic 3-by-3 puzzle in the fewest slides, with three complete examples. |
| Trees | [BFS foundations](trees/bfs/foundations/) | Read each level in child-list order, with three complete examples and a waiting-queue checkpoint. |
| Trees | [BFS printing](trees/bfs/printing/) | Print a five-node tree level by level, then try empty, singleton and wide trees. |
| Data structures | [Bloom Filter](data_structures/bloom_filter/foundations/) | Reproduce a real false positive, a definite absence, and the unsafe deletion example. |
| Data structures | [Top K: three largest files](data_structures/top_k/three_largest_files/) | Stream ten file records through a heap of three, then test ties, empty inputs and arbitrary capacities. |
| Data structures | [LRU Cache](data_structures/lru_cache/foundations/) | Follow picture requests, inspect hits and misses, move linked nodes, and reproduce the all-miss cycle. |
| Data structures | [LRU API cache](data_structures/lru_cache/api_cache/) | Serve real SQLite product records, count executed queries, and compare a three-slot cache with a four-product cycle. |
| Data structures | [LRU shopping cache](data_structures/lru_cache/shopping/) | Compare LRU with FIFO, follow node-preserving updates, and test zero capacity. |
| Data structures | [LRU three-slot walkthrough](data_structures/lru_cache/three_slot_walkthrough/) | Trace every helper, update and eviction, with space freed before insertion. |
| Data structures | [Cache Lab shopping Shorts](data_structures/cache_policies/shopping_shorts/) | Run seven independent examples of hits/misses, FIFO/LRU/LFU, thrashing and stale-price invalidation. |

## Run an example

Use Python 3.10 or newer. The current examples use only the standard library.
Download the repository or clone it, then run these commands from its root:

```sh
python3 graphs/a_star/foundations/a_star.py
python3 -m unittest discover -s graphs/a_star/foundations -v
```

Each lesson folder contains the complete implementation, runnable inputs, a README
with the contract and expected results, and correctness tests. Python files credit
BigOCast and Moein. Comments explain the decisions that matter to the algorithm.

Folders are grouped by category and algorithm. Distinct lessons about the same
algorithm keep separate example folders, such as `graphs/a_star/foundations/`.
Problem-solution videos belong under a separate `problems/` category when added.

Video descriptions and pinned comments link directly to the matching folder at a
fixed commit, so the example stays consistent with the explanation. The default
branch contains the latest corrections and additions.

More visual algorithms and the newsletter: [bigocast.com](https://bigocast.com).

## License

MIT, following the existing BigOCast public code repository. See [LICENSE](LICENSE).
