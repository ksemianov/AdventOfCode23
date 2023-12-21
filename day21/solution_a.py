from collections import deque


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


def bfs(graph: list[str], start: tuple[int, int, int]) -> int:
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
            if not (
                0 <= ni < n_rows and 0 <= nj < n_cols and graph[ni][nj] in {".", "S"}
            ):
                continue

            next_node = (ni, nj, steps - 1)
            if next_node in visited:
                continue

            q.append(next_node)
            visited.add(next_node)

    visited_coords = set((i, j) for i, j, steps in visited if steps == 0)
    return len(visited_coords)


def main():
    text = get_text()
    graph = text.split("\n")
    start_i, start_j = find_start(graph)
    result = bfs(graph, (start_i, start_j, 64))
    return result


if __name__ == "__main__":
    print(main())
