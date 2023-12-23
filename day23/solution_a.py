from dataclasses import dataclass
from typing import Optional
import sys


@dataclass(frozen=True)
class Coord:
    i: int
    j: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.i + other.i, self.j + other.j)


def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


def find_dot_column(line: str) -> int:
    return next(j for j, c in enumerate(line) if c == ".")


def max_steps(
    graph: list[str], visited: set[Coord], current: Coord, end: Coord
) -> Optional[int]:
    if current == end:
        return 0

    current_c = graph[current.i][current.j]
    visited.add(current)

    if current_c == ".":
        directions = [Coord(-1, 0), Coord(1, 0), Coord(0, -1), Coord(0, 1)]
    elif current_c == "^":
        directions = [Coord(-1, 0)]
    elif current_c == ">":
        directions = [Coord(0, 1)]
    elif current_c == "v":
        directions = [Coord(1, 0)]
    elif current_c == "<":
        directions = [Coord(0, -1)]
    else:
        raise RuntimeError(f"Unknown directions for node {current_c}")

    result = None

    for direction in directions:
        destination = current + direction
        if not (
            0 <= destination.i < len(graph)
            and 0 <= destination.j < len(graph[0])
            and graph[destination.i][destination.j] != "#"
        ):
            continue

        if destination in visited:
            continue

        candidate = max_steps(graph, visited, destination, end)
        if candidate is not None:
            if result:
                result = max(result, candidate)
            else:
                result = candidate

    visited.remove(current)

    if result is not None:
        return result + 1


def main():
    text = get_text()
    graph = text.split("\n")
    start = Coord(0, find_dot_column(graph[0]))
    end = Coord(len(graph) - 1, find_dot_column(graph[-1]))
    print(start, end)

    sys.setrecursionlimit(1_000_000)
    result = max_steps(graph, set(), start, end)

    return result


if __name__ == "__main__":
    print(main())
