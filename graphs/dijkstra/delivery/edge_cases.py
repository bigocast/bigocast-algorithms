"""BigOCast | Moein. Exact advanced-lesson cases, using the same function."""
from dijkstra import GRAPH, shortest_path

ZERO_CYCLE = {
    "S": [("A", 1), ("T", 2)],
    "A": [("B", 0)],
    "B": [("A", 0), ("T", 1)],
    "T": [],
}
NEGATIVE = {"S": [("T", 2), ("B", 5)], "B": [("T", -4)], "T": []}
UNREACHABLE = {
    node: [(neighbor, weight) for neighbor, weight in roads if neighbor != "Home"]
    for node, roads in GRAPH.items()
}

if __name__ == "__main__":
    print("Tied routes and zero cycle:", shortest_path(ZERO_CYCLE, "S", "T"))
    print("Unreachable:", shortest_path(UNREACHABLE, "Depot", "Home"))
    print("Already at goal:", shortest_path(GRAPH, "Depot", "Depot"))
    try:
        shortest_path(NEGATIVE, "S", "T")
    except ValueError as error:
        print("Negative edge rejected:", error)
