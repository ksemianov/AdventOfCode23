def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


def hash(string: str) -> int:
    result = 0

    for char in string:
        result += ord(char)
        result *= 17
        result %= 256

    return result


def main():
    text = get_text()

    result = sum(hash(s) for s in text.split(","))

    return result


if __name__ == "__main__":
    print(main())
