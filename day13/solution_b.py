from typing import Optional


def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


def process_pattern(pattern: str, original_line: Optional[int]) -> int:
    pattern = pattern.split("\n")
    n_rows = len(pattern)
    n_cols = len(pattern[0])

    for row in range(1, n_rows):
        if original_line == row * 100:
            continue

        is_valid = True

        for j in range(n_cols):
            for i in range(n_rows):
                mi = 2 * row - i - 1
                if mi >= n_rows or mi < 0:
                    continue

                if pattern[i][j] != pattern[mi][j]:
                    is_valid = False
                    break

            if not is_valid:
                break

        if is_valid:
            return 100 * row

    for col in range(1, n_cols):
        if original_line == col:
            continue

        is_valid = True

        for i in range(n_rows):
            for j in range(n_cols):
                mj = 2 * col - j - 1
                if mj >= n_cols or mj < 0:
                    continue

                if pattern[i][j] != pattern[i][mj]:
                    is_valid = False
                    break

            if not is_valid:
                break

        if is_valid:
            return col

    return 0


def main():
    text = get_text()

    patterns = text.split("\n\n")

    result = 0

    for pattern in patterns:
        original_line = process_pattern(pattern, None)
        for index, char in enumerate(pattern):
            if char == "\n":
                continue

            if char == "#":
                opposite_char = "."
            elif char == ".":
                opposite_char = "#"
            else:
                raise ValueError(f"Unknown char {char}")

            fixed_pattern = pattern[:index] + opposite_char + pattern[index + 1:]
            res = process_pattern(fixed_pattern, original_line)
            if res:
                # print(fixed_pattern)
                # print(res)
                # print()
                result += res
                break

    return result


if __name__ == "__main__":
    print(main())
