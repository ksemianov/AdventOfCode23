import re
from typing import Optional


def get_lines() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def parse_pattern(line: str, pattern: str) -> Optional[int]:
    matches = re.findall(pattern, line)
    if matches:
        return int(matches[0])


def parse_draw(line: str) -> tuple[int, int, int]:
    red = parse_pattern(line, r"(\d+) red") or 0
    green = parse_pattern(line, r"(\d+) green") or 0
    blue = parse_pattern(line, r"(\d+) blue") or 0
    return red, green, blue


def process_line(line: str) -> int:
    max_red = 0
    max_green = 0
    max_blue = 0

    for draw in line.split(";"):
        red, green, blue = parse_draw(draw.strip())
        max_red = max(max_red, red)
        max_green = max(max_green, green)
        max_blue = max(max_blue, blue)

    return max_red * max_green * max_blue


def main():
    result = 0

    for line in get_lines():
        result += process_line(line)

    return result


if __name__ == "__main__":
    print(main())
