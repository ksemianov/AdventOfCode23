from copy import deepcopy
from enum import Enum
from typing import Optional


def get_lines() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def find_starting_point(graph: list[str]) -> Optional[tuple[int, int]]:
    for i, row in enumerate(graph):
        for j, node in enumerate(row):
            if node == "S":
                return i, j


class Direction(Enum):
    left = "l"
    top = "t"
    right = "r"
    bottom = "b"


NODE_TO_DIRECTION_MAP = {
    "|": [Direction.top, Direction.bottom],
    "-": [Direction.left, Direction.right],
    "L": [Direction.top, Direction.right],
    "J": [Direction.top, Direction.left],
    "7": [Direction.left, Direction.bottom],
    "F": [Direction.right, Direction.bottom],
    ".": [],
    "S": [Direction.left, Direction.top, Direction.right, Direction.bottom],
}

DIRECTION_TO_OFFSET_MAP = {
    Direction.left: (0, -1),
    Direction.top: (-1, 0),
    Direction.right: (0, 1),
    Direction.bottom: (1, 0),
}

DIRECTION_INVERSE_MAP = {
    Direction.left: Direction.right,
    Direction.top: Direction.bottom,
    Direction.right: Direction.left,
    Direction.bottom: Direction.top,
}


def allowed_directions(node: str) -> list[Direction]:
    return NODE_TO_DIRECTION_MAP[node]


def build_offset(direction: Direction) -> tuple[int, int]:
    return DIRECTION_TO_OFFSET_MAP[direction]


def build_direction_inverse(direction: Direction) -> Direction:
    return DIRECTION_INVERSE_MAP[direction]


def build_distances(
    graph: list[str], start: tuple[int, int]
) -> list[list[Optional[int]]]:
    distances: list[list[Optional[int]]] = [
        [None for _ in range(len(x))] for x in graph
    ]
    start_i, start_j = start
    distances[start_i][start_j] = 0

    visited = set()
    queue = [start]

    while queue:
        current = queue.pop(0)
        visited.add(current)
        i, j = current
        node = graph[i][j]
        distance = distances[i][j]
        directions = allowed_directions(node)
        for direction in directions:
            di, dj = build_offset(direction)
            i2 = i + di
            j2 = j + dj
            destination = (i2, j2)
            destination_node = graph[i2][j2]
            if build_direction_inverse(direction) not in allowed_directions(
                destination_node
            ):
                # pipes do not connect
                continue

            if not (0 <= i2 < len(distances) and 0 <= j2 < len(distances[i2])):
                # out of bounds
                continue

            destination_distance = distances[i2][j2]
            if destination_distance is None:
                distances[i2][j2] = distance + 1
            else:
                distances[i2][j2] = min(distance + 1, destination_distance)

            if destination not in visited:
                # bfs
                queue.append(destination)

    return distances


def find_maximal_row_distance(
    row_distances: list[Optional[int]],
) -> Optional[tuple[int, int]]:
    try:
        return max(
            ((j, x) for j, x in enumerate(row_distances) if x), key=lambda item: item[1]
        )
    except ValueError:
        return None


def find_maximal_distance(
    distances: list[list[Optional[int]]],
) -> Optional[tuple[int, int, int]]:
    row_distances = [find_maximal_row_distance(x) for x in distances]

    try:
        return max(
            ((i, jx[0], jx[1]) for i, jx in enumerate(row_distances) if jx),
            key=lambda item: item[2],
        )
    except ValueError:
        return None


def find_main_loop(
    distances: list[list[Optional[int]]],
    max_distance: tuple[int, int, int],
) -> list[list[bool]]:
    result: list[list[bool]] = [[False for _ in range(len(x))] for x in distances]

    queue = [max_distance]

    while queue:
        current = queue.pop(0)
        i, j, distance = current
        result[i][j] = 1

        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            i2, j2 = i + di, j + dj

            if not (0 <= i2 < len(distances) and 0 <= j2 < len(distances[i2])):
                # out of bounds
                continue

            destination_distance = distances[i2][j2]
            if destination_distance == distance - 1:
                destination = (i2, j2, destination_distance)
                queue.append(destination)

    return result


def simplify_graph_inplace(graph: list[str], main_loop: list[list[bool]]) -> list[str]:
    for i, row in enumerate(graph):
        new_row = ""

        for j, node in enumerate(row):
            if not main_loop[i][j]:
                new_row += "."
            else:
                new_row += node

        graph[i] = new_row

    return graph


def count_enclosed_row(row: str, next_row: str) -> int:
    result = 0
    intersections = 0

    for j, node in enumerate(row):
        next_node = next_row[j]

        if Direction.bottom in allowed_directions(
            node
        ) and Direction.top in allowed_directions(next_node):
            intersections += 1

        if node == ".":
            if intersections % 2 == 1:
                result += 1
        #         print("I", end="")
        #     else:
        #         print("0", end="")
        # else:
        #     print(node, end="")

    # print()

    return result


def main():
    graph = [x.strip() for x in get_lines()]

    start = find_starting_point(graph)
    if start is None:
        raise RuntimeError("Unable to find the start point")

    distances = build_distances(graph, start)
    max_distance = find_maximal_distance(distances)
    main_loop = find_main_loop(distances, max_distance)
    simplify_graph_inplace(graph, main_loop)

    result = 0
    n_rows = len(graph)
    for i, row in enumerate(graph):
        if i == n_rows - 1:
            break

        result += count_enclosed_row(row, graph[i + 1])

    return result


if __name__ == "__main__":
    print(main())
