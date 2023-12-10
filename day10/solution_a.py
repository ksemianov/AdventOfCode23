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

    # vis = ""
    # for distance_row in distances:
    #     for distance in distance_row:
    #         if distance is not None:
    #             vis += f"{distance:>5}"
    #         else:
    #             vis += "     "
    #     vis += "\n"
    # print(vis)

    return distances


def find_maximal_row_distance(row_distances: list[Optional[int]]) -> Optional[int]:
    try:
        return max(x for x in row_distances if x)
    except ValueError:
        return None


def find_maximal_distance(distances: list[list[Optional[int]]]) -> Optional[int]:
    row_distances = [find_maximal_row_distance(x) for x in distances]

    try:
        return max(x for x in row_distances if x)
    except ValueError:
        return None


def main():
    graph = [x.strip() for x in get_lines()]

    start = find_starting_point(graph)
    if start is None:
        raise RuntimeError("Unable to find the start point")

    distances = build_distances(graph, start)
    result = find_maximal_distance(distances)

    return result


if __name__ == "__main__":
    print(main())
