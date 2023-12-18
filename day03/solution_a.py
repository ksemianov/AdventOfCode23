import re
from typing import Optional


def get_lines() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def has_symbol(
    line: str,
    start: int,
    end: int,
    banned_symbols: set[str] = [str(x) for x in range(10)] + [".", "\n"],
) -> bool:
    start = max(0, start)
    end = min(len(line) - 1, end)

    for i in range(start, end + 1):
        char = line[i]
        if char not in banned_symbols:
            return True

    return False


def process_line(line: str, top_line: Optional[str], bottom_line: Optional[str]) -> int:
    result = 0

    for match in re.finditer(r"(\d+)", line):
        group = match.group()
        start_index = match.start()
        end_index = match.end()

        has_adjacent_symbol = False

        if top_line:
            has_adjacent_symbol = has_adjacent_symbol or has_symbol(
                top_line, start_index - 1, end_index
            )

        if bottom_line:
            has_adjacent_symbol = has_adjacent_symbol or has_symbol(
                bottom_line, start_index - 1, end_index
            )

        has_adjacent_symbol = has_adjacent_symbol or has_symbol(
            line, start_index - 1, start_index - 1
        )
        has_adjacent_symbol = has_adjacent_symbol or has_symbol(
            line, end_index, end_index
        )

        if has_adjacent_symbol:
            result += int(group)

    return result


def main():
    result = 0

    lines = get_lines()
    n_lines = len(lines)

    for i in range(n_lines):
        line = lines[i]

        top_line = None
        if i > 0:
            top_line = lines[i - 1]

        bottom_line = None
        if i < n_lines - 1:
            bottom_line = lines[i + 1]

        result += process_line(line, top_line, bottom_line)

    return result


if __name__ == "__main__":
    print(main())
