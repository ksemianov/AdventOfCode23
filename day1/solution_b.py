valid_spelled_digits = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def get_lines() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def extract_digits(line: str) -> [int]:
    result = []

    for pos, char in enumerate(line):
        if char.isdigit():
            result.append(int(char))
        else:
            line_view = line[pos:]
            for prefix, digit in valid_spelled_digits.items():
                if line_view.startswith(prefix):
                    result.append(digit)
                    break

    return result


def process_line(line: str) -> int:
    digits = extract_digits(line)
    result = digits[0] * 10 + digits[-1]
    return result


def main() -> int:
    result = 0

    for line in get_lines():
        result += process_line(line)

    return result


if __name__ == "__main__":
    print(main())
