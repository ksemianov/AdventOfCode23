import re


def get_lines() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def extract_numbers(line: str) -> [int]:
    return [int(x) for x in re.findall(r"(\d+)", line)]


def process_line(line: str) -> int:
    card_part, numbers_part = line.split(":")
    winning_part, actual_part = numbers_part.split("|")

    winning = set(extract_numbers(winning_part))

    points = 0
    for number in extract_numbers(actual_part):
        if number in winning:
            if points == 0:
                points = 1
            else:
                points *= 2

    return points


def main():
    result = 0

    for line in get_lines():
        result += process_line(line)

    return result


if __name__ == "__main__":
    print(main())
