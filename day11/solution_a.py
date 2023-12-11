def get_lines() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def extract_galaxy_locations(
    map: list[str], expansion_factor: int
) -> list[tuple[int, int]]:
    n_rows = len(map)
    n_cols = len(map[0])

    is_empty_row = [True for _ in range(n_rows)]
    is_empty_col = [True for _ in range(n_cols)]

    for row in range(n_rows):
        for col in range(n_cols):
            if map[row][col] == "#":
                is_empty_row[row] = False
                is_empty_col[col] = False

    result = []
    row_offset = 0

    for row in range(n_rows):
        col_offset = 0

        if is_empty_row[row]:
            row_offset += expansion_factor - 1

        for col in range(n_cols):
            if is_empty_col[col]:
                col_offset += expansion_factor - 1

            if map[row][col] == "#":
                result.append((row + row_offset, col + col_offset))

    return result


def main():
    map = [x.strip() for x in get_lines()]
    locs = extract_galaxy_locations(map, expansion_factor=2)
    n_locs = len(locs)

    result = 0

    for i in range(n_locs):
        for j in range(i + 1, n_locs):
            loc1 = locs[i]
            loc2 = locs[j]
            distance = abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])
            result += distance

    return result


if __name__ == "__main__":
    print(main())
