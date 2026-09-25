# BigOCast algorithms

Complete Python examples from BigOCast, by Moein. Run the algorithms, change the
inputs, and follow the same decisions explained in the videos.

## Browse the lessons

| Category | Lesson | What you can try |
| --- | --- | --- |
| Graph search | [A* foundations](graphs/a_star/foundations/) | Find a shortest route around a wall, then try an open floor. |
| Graph search | [A* sliding puzzle](graphs/a_star/sliding_puzzle/) | Solve the classic 3-by-3 puzzle in the fewest slides, with three complete examples. |
| Trees | [BFS foundations](trees/bfs/foundations/) | Read each level in child-list order, with three complete examples and a waiting-queue checkpoint. |
| Data structures | [Bloom Filter](data_structures/bloom_filter/foundations/) | Reproduce a real false positive, a definite absence, and the unsafe deletion example. |

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
