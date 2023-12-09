def get_lines() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def predict(seq: list[int]) -> int:
    if not seq or all(x == 0 for x in seq):
        return 0

    diff = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
    return seq[0] - predict(diff)


def process_line(line: str) -> int:
    seq = [int(x) for x in line.split(" ")]
    prediction = predict(seq)
    return prediction


def main():
    lines = [x.strip() for x in get_lines()]

    result = 0

    for line in lines:
        result += process_line(line)

    return result


if __name__ == "__main__":
    print(main())
