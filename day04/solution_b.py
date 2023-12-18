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

    matches = 0
    for number in extract_numbers(actual_part):
        if number in winning:
            matches += 1

    return matches


def main():
    matches_for_lines = [process_line(x) for x in get_lines()]

    result = 0
    count = {x: 1 for x in range(len(matches_for_lines))}

    for i, matches_for_line in enumerate(matches_for_lines):
        result += count[i]
        for j in range(matches_for_line):
            count[i + j + 1] += count[i]

    return result


if __name__ == "__main__":
    print(main())
