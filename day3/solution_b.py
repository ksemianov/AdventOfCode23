import re
from typing import Optional


def get_lines() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def find_adjacent(line: str, start: int, end: int) -> list[int]:
    result = []

    for match in re.finditer(r"(\d+)", line):
        match_group = int(match.group())
        match_start = match.start()
        match_end = match.end() - 1

        if start <= match_start <= end or start <= match_end <= end:
            result.append(match_group)

    return result


def process_line(line: str, top_line: Optional[str], bottom_line: Optional[str]) -> int:
    result = 0

    for match in re.finditer(r"\*", line):
        gear_candidate = match.start()
        adjacent = []

        if top_line:
            adjacent += find_adjacent(top_line, gear_candidate - 1, gear_candidate + 1)

        if bottom_line:
            adjacent += find_adjacent(
                bottom_line, gear_candidate - 1, gear_candidate + 1
            )

        adjacent += find_adjacent(line, gear_candidate - 1, gear_candidate - 1)
        adjacent += find_adjacent(line, gear_candidate + 1, gear_candidate + 1)

        if len(adjacent) == 2:
            a, b = adjacent
            result += a * b

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
