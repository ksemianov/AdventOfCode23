from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Coord:
    i: int
    j: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.i + other.i, self.j + other.j)

    def __neg__(self) -> "Coord":
        return Coord(-self.i, -self.j)


directions = [Coord(-1, 0), Coord(1, 0), Coord(0, -1), Coord(0, 1)]


def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


def find_dot_column(line: str) -> int:
    return next(j for j, c in enumerate(line) if c == ".")


def find_junctions(graph: list[str]) -> list[Coord]:
    result = []

    n_rows = len(graph)
    n_cols = len(graph[0])

    for i in range(1, n_rows - 1):
        for j in range(1, n_cols - 1):
            if graph[i][j] == "#":
                continue

            valid_count = 0
            current = Coord(i, j)
            for direction in directions:
                destination = current + direction
                if graph[destination.i][destination.j] != "#":
                    valid_count += 1

            if valid_count > 2:
                result.append(current)

    return result


def find_simple_path(
    graph: list[str], start: Coord, end: Coord, direction: Coord
) -> Optional[int]:
    result = 1
    current = start + direction
    if graph[current.i][current.j] == "#":
        return None

    last_direction = direction

    while True:
        valid_directions = []
        for direction in directions:
            if last_direction is not None and direction == -last_direction:
                continue

            destination = current + direction
            if not (
                0 <= destination.i < len(graph) and 0 <= destination.j < len(graph[0])
            ):
                continue

            if graph[destination.i][destination.j] != "#":
                valid_directions.append(direction)

        if len(valid_directions) != 1:
            return None

        direction = valid_directions[0]
        destination = current + direction
        result += 1
        current = destination
        last_direction = direction
        if current == end:
            return result


def max_steps(
    graph: dict[Coord, list[tuple[Coord, int]]],
    visited: set[Coord],
    current: Coord,
    end: Coord,
) -> Optional[int]:
    if current == end:
        return 0

    visited.add(current)

    result = None

    for destination, distance in graph[current]:
        if destination not in visited:
            candidate = max_steps(graph, visited, destination, end)

            if candidate is not None:
                candidate += distance
                if result is not None:
                    result = max(result, candidate)
                else:
                    result = candidate

    visited.remove(current)

    return result


def build_simple_graph(
    graph: list[str], nodes: list[Coord]
) -> dict[Coord, list[tuple[Coord, int]]]:
    result = {}

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            node_src = nodes[i]
            node_dst = nodes[j]
            for direction in directions:
                distance = find_simple_path(graph, node_src, node_dst, direction)
                if distance:
                    if node_src not in result:
                        result[node_src] = []
                    if node_dst not in result:
                        result[node_dst] = []
                    result[node_src].append((node_dst, distance))
                    result[node_dst].append((node_src, distance))

    return result


def main():
    text = get_text()
    graph = text.split("\n")
    start = Coord(0, find_dot_column(graph[0]))
    end = Coord(len(graph) - 1, find_dot_column(graph[-1]))
    junctions = find_junctions(graph)
    nodes = [start] + junctions + [end]
    simple_graph = build_simple_graph(graph, nodes)

    result = max_steps(simple_graph, set(), start, end)

    return result


if __name__ == "__main__":
    print(main())
