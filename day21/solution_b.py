from collections import deque
import numpy as np


def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


def find_start(graph: list[str]) -> tuple[int, int]:
    n_rows = len(graph)
    n_cols = len(graph)

    for i in range(n_rows):
        for j in range(n_cols):
            if graph[i][j] == "S":
                return i, j

    raise RuntimeError("No start node")


def bfs(graph: list[str], start: tuple[int, int, int]) -> list[int]:
    n_rows = len(graph)
    n_cols = len(graph)

    visited = set()
    q = deque([start])

    while q:
        i, j, steps = q.popleft()
        if steps <= 0:
            continue

        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if graph[ni % n_rows][nj % n_cols] not in {".", "S"}:
                continue

            next_node = (ni, nj, steps - 1)
            if next_node in visited:
                continue

            q.append(next_node)
            visited.add(next_node)

    result = []
    for steps in range(start[2]):
        result.append(len(set((i, j) for i, j, s in visited if s == steps)))
    result.append(1)

    return result[::-1]


def main():
    text = get_text()
    graph = text.split("\n")
    start_i, start_j = find_start(graph)

    # 26501365 = 131 * 202300 + 65
    # 65 is the offset
    # 131 is the cycle lengh
    result = bfs(graph, (start_i, start_j, 65 + 131 * 2))
    coeffs = result[65::131]  # [3799, 34047, 94475]
    poly = [int(x + 0.499) for x in np.polyfit([0, 1, 2], coeffs, deg=2)]
    x = 202300
    return (x**2) * poly[0] + x * poly[1] + poly[2]


if __name__ == "__main__":
    print(main())
