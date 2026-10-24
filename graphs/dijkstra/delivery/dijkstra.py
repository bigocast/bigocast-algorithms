"""BigOCast | Moein.
Directed paths with integer weights.
"""

from heapq import heappop, heappush
from math import inf


def validate_graph(graph, start, goal):
    """String IDs; nonnegative integer weights."""
    for node in graph:
        if not isinstance(node, str):
            raise ValueError("Use string node IDs")
    if start not in graph or goal not in graph:
        raise ValueError("Unknown start or goal")
    for roads in graph.values():
        for neighbor, weight in roads:
            if neighbor not in graph:
                raise ValueError("Unknown endpoint")
            if type(weight) is not int or weight < 0:
                raise ValueError(
                    "Nonnegative integers required"
                )


def rebuild_path(previous, goal):
    path = [goal]
    while path[-1] in previous:
        path.append(previous[path[-1]])
    path.reverse()
    return path


def shortest_path(graph, start, goal):
    """Return (cost, path), or (infinity, [])."""
    validate_graph(graph, start, goal)
    distances = {node: inf for node in graph}
    distances[start] = 0
    previous = {}
    pending = [(0, start)]

    while pending:
        cost, node = heappop(pending)
        if cost != distances[node]:
            continue
        if node == goal:
            path = rebuild_path(previous, goal)
            return cost, path

        for neighbor, weight in graph[node]:
            candidate = cost + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                previous[neighbor] = node
                offer = (candidate, neighbor)
                heappush(pending, offer)

    return inf, []



# The shared delivery map.
# Road weights are kilometers.
GRAPH = {
    "Depot": [
        ("Park", 2), ("Bridge", 6),
        ("Market", 4), ("Home", 12),
    ],
    "Park": [("Bridge", 1)],
    "Bridge": [("Home", 5)],
    "Market": [("Home", 3)],
    "Home": [],
}

if __name__ == "__main__":
    cost, route = shortest_path(
        GRAPH, "Depot", "Home"
    )
    print(cost, route)
