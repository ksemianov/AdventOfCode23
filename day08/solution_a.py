from dataclasses import dataclass


@dataclass
class Junction:
    left: str
    right: str


def get_lines() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def process_line(line: str) -> tuple[str, Junction]:
    src, lr_part = line.split(" = ")
    left, right = lr_part.strip("()").split(", ")
    return src, Junction(left, right)


def main():
    lines = [x.strip() for x in get_lines()]
    instructions = lines[0]
    n_instructions = len(instructions)

    nodes = {k: v for k, v in [process_line(x) for x in lines[2:]]}

    step = 0
    location = "AAA"

    while location != "ZZZ":
        instruction = instructions[step % n_instructions]

        if instruction == "L":
            location = nodes[location].left
        elif instruction == "R":
            location = nodes[location].right
        else:
            raise ValueError("Invalid instruction")

        step += 1

    return step


if __name__ == "__main__":
    print(main())
