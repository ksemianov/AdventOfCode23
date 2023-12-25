from collections import deque
from functools import reduce

import graphviz


def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


def parse_line(line: str) -> list[tuple[str, str]]:
    key_part, value_part = line.split(": ")

    result = []

    for value in value_part.split(" "):
        result.append((key_part, value))
        # result.append((value, key_part))

    return result


def render(nodes: set[str], edges: list[tuple[str, str]]) -> None:
    dot = graphviz.Graph(engine="sfdp")
    for node in nodes:
        dot.node(node)
    for node_a, node_b in edges:
        dot.edge(node_a, node_b)

    path = "graph"
    dot.render(path)


def count_components(edges: list[tuple[str, str]]) -> tuple[int, int]:
    graph = {}
    for node_a, node_b in edges:
        if node_a not in graph:
            graph[node_a] = set()
        if node_b not in graph:
            graph[node_b] = set()

        graph[node_a].add(node_b)
        graph[node_b].add(node_a)

    start = next(iter(graph.keys()))
    visited = {start}
    q = deque([start])
    while q:
        current = q.popleft()
        for destination in graph[current]:
            if destination not in visited:
                q.append(destination)
                visited.add(destination)

    n_visited = len(visited)
    n_total = len(graph)

    return n_visited, n_total - n_visited


def main():
    text = get_text()
    edges = reduce(lambda x, y: x + y, (parse_line(line) for line in text.split("\n")))
    nodes = {node for node, _ in edges}

    # from render:
    for_removal = [
        ("fdb", "psj"),
        ("psj", "fdb"),
        ("rmt", "nqh"),
        ("nqh", "rmt"),
        ("trh", "ltn"),
        ("ltn", "trh"),
    ]
    # for_removal = [
    #     ("hfx", "pzl"),
    #     ("pzl", "hfx"),
    #     ("bvb", "cmg"),
    #     ("cmg", "bvb"),
    #     ("nvd", "jqt"),
    #     ("jqt", "nvd"),
    # ]
    new_edges = []
    for edge in edges:
        if edge not in for_removal:
            new_edges.append(edge)
    edges = new_edges

    group1, group2 = count_components(edges)
    return group1 * group2


if __name__ == "__main__":
    print(main())
