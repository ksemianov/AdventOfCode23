def get_lines() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def extract_digits(line: str) -> [int]:
    result = [int(x) for x in filter(lambda x: x.isdigit(), line)]
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
