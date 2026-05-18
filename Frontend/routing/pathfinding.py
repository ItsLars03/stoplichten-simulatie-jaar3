"""Shared pathfinding helpers for route generation."""


def shortest_path(graph, start, goal):
    """Return the shortest node path between one point and another using breath first search."""
    queue = [(start, [start])]
    visited = {start}
    while queue:
        node, path = queue.pop(0)
        if node == goal:
            return path
        for nxt in graph.get(node, []):
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [nxt]))
    return None


def build_boundary_routes(graph, segments, boundary_nodes):
    """Build routes between every pair of boundary nodes using shared segments."""
    routes = []
    for start in boundary_nodes:
        for end in boundary_nodes:
            if start == end:
                continue
            node_path = shortest_path(graph, start, end)
            if not node_path:
                continue
            keys = []
            for a, b in zip(node_path, node_path[1:]):
                segment = segments[(a, b)]
                if keys and segment[0] == keys[-1]:
                    keys.extend(segment[1:])
                else:
                    keys.extend(segment)
            routes.append((f"{start}->{end}", keys))
    return routes

