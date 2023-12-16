from tqdm import tqdm


def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


def bfs(graph: list[str], start: tuple[int, int, str]) -> set[tuple[int, int, str]]:
    n_rows = len(graph)
    n_cols = len(graph[0])

    queue = [start]
    visited = {start}

    def process_candidate(candidate: tuple[int, int, str]) -> None:
        i_coord, j_coord, _ = candidate
        if not (0 <= i_coord < n_rows and 0 <= j_coord < n_cols):
            return
        if candidate in visited:
            return
        # print(candidate)
        queue.append(candidate)
        visited.add(candidate)

    while queue:
        current = queue.pop(0)

        i, j, direction = current
        node = graph[i][j]

        if node == "/":
            direction = {
                "l": "d",
                "u": "r",
                "r": "u",
                "d": "l",
            }[direction]
            node = "."
        elif node == "\\":
            direction = {
                "l": "u",
                "d": "r",
                "r": "d",
                "u": "l",
            }[direction]
            node = "."
        elif node == "-" and direction in {"l", "r"}:
            node = "."
        elif node == "|" and direction in {"u", "d"}:
            node = "."

        if node == ".":
            di, dj = {
                "l": (0, -1),
                "u": (-1, 0),
                "r": (0, 1),
                "d": (1, 0),
            }[direction]
            ni, nj = i + di, j + dj
            route = (ni, nj, direction)
            process_candidate(route)
        elif node == "-":
            for di, dj, direction in [(0, -1, "l"), (0, 1, "r")]:
                ni, nj = i + di, j + dj
                route = (ni, nj, direction)
                process_candidate(route)
        elif node == "|":
            for di, dj, direction in [(-1, 0, "u"), (1, 0, "d")]:
                ni, nj = i + di, j + dj
                route = (ni, nj, direction)
                process_candidate(route)
        else:
            raise RuntimeError("Something went wrong")

    return visited


def main():
    text = get_text()
    lines = text.split("\n")
    n_rows = len(lines)
    n_cols = len(lines[0])

    start_candidates = []
    for i in range(n_rows):
        start_candidates.append((i, 0, "r"))
        start_candidates.append((i, n_cols - 1, "l"))
    for j in range(n_cols):
        start_candidates.append((0, j, "d"))
        start_candidates.append((n_rows - 1, j, "u"))

    result = 0
    for start in tqdm(start_candidates):
        visited = bfs(lines, start)
        visited = set((i, j) for i, j, direction in visited)
        result = max(result, len(visited))

    return result


if __name__ == "__main__":
    print(main())
