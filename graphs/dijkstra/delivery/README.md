# Dijkstra: delivery route and the guarantees behind it

BigOCast | Moein. Companion to **Dijkstra’s Algorithm Explained with Python** and
**Why Dijkstra Works (and When It Fails)**. Video links will be added after publication.

Run from the repository root with Python 3.10 or newer. Only the standard library is needed.

```sh
python3 graphs/dijkstra/delivery/dijkstra.py
python3 graphs/dijkstra/delivery/edge_cases.py
python3 -m unittest discover -s graphs/dijkstra/delivery -v
```

The delivery example prints:

```text
7 ['Depot', 'Market', 'Home']
```

The arrows are directed roads; weights are kilometers. The map has five places and
seven roads. Depot initially offers Park 2, Bridge 6, Market 4 and Home 12. Park
improves Bridge to 3. Bridge improves Home to 8; Market improves it to 7. The old
Bridge 6 offer is popped and skipped before Home 7 returns. Two old Home offers
remain when this single-target search stops.

`shortest_path(graph, start, goal)` returns `(cost, path)`, or `(inf, [])` if a valid
goal is unreachable. Start equal to goal returns `(0, [start])` after validation.
Every node ID must be a string, every endpoint must exist, and weights must be
nonnegative integers. Booleans are rejected as weights. Invalid input raises
`ValueError`. The graph must be a complete adjacency dictionary: even a place with
no outgoing roads needs an empty list. The implementation does not mutate it.

Each strict improvement records a predecessor and pushes an immutable heap offer.
Old offers stay in the heap until popped. A cost different from the current distance
is skipped. The shown implementation checks the goal after this guard. Under the
nonnegative contract, the usable minimum distance is final.

Zero weights and equal routes are allowed. Only `<` creates an improvement; `<=`
can endlessly requeue equal-cost offers around a zero-cost cycle. The function
returns one shortest route. It does not enumerate ties. Equal heap priorities use
the string names as Python tuple tie-breakers.

Let V be the number of nodes and E the number of directed adjacency entries.
Validation and initialization take O(V + E). Each processed node's outgoing roads
are scanned once; stale offers are skipped before the road loop. There are at most
E strict improvements and O(E) heap operations. For E >= 1, total time is
O(V + E log(E + 1)); an edgeless valid graph takes O(V). On a simple graph the common
O((V + E) log V) bound is also valid (with the constant-size case understood).
The lazy heap can contain O(E) offers, so auxiliary space is O(V + E), including
the distance/predecessor dictionaries and returned path. Input adjacency lists
also occupy O(V + E). These bounds use the usual constant-cost arithmetic and
identifier-comparison model; large integers or long strings can add cost.

Try changing the Market-to-Home weight, isolating Home, or running the zero-cycle
case in `edge_cases.py`. A negative edge is rejected; it is not a supported shortcut
to extending Dijkstra to negative costs. Tests include an independent Bellman-Ford
oracle over deterministic random nonnegative graphs.
