import re


def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


def get_hash(string: str) -> int:
    result = 0

    for char in string:
        result += ord(char)
        result *= 17
        result %= 256

    return result


def main():
    text = get_text()

    boxes = {k: dict() for k in range(256)}

    for step in text.split(","):
        label_match = re.match("^[a-z]+", step)
        label = label_match.group()
        command = step[label_match.end()]
        hash_value = get_hash(label)

        if command == "=":
            focal_length = int(step[label_match.end() + 1:])
            boxes[hash_value][label] = focal_length
        elif command == "-":
            if label in boxes[hash_value]:
                del boxes[hash_value][label]
        else:
            ValueError(f"Unknown command {command}")

        # print([(k, v) for k, v in boxes.items() if v])

    result = 0

    for box_number, box in boxes.items():
        for slot, (label, focal_length) in enumerate(box.items()):
            product = (box_number + 1) * (slot + 1) * focal_length
            # print(product)
            result += product

    return result


if __name__ == "__main__":
    print(main())
