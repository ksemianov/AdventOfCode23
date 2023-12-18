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


def get_step_count(location: str, instructions: str, nodes: dict[str, Junction]) -> int:
    n_instructions = len(instructions)
    step = 0

    while location[-1] != "Z":
        instruction = instructions[step % n_instructions]

        if instruction == "L":
            location = nodes[location].left
        elif instruction == "R":
            location = nodes[location].right
        else:
            raise ValueError("Invalid instruction")

        step += 1

    return step


def gcd(a: int, b: int) -> int:
    if b > a:
        b, a = a, b

    a = a % b

    if a == 0:
        return b
    else:
        return gcd(a, b)


def lcd(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def main():
    lines = [x.strip() for x in get_lines()]
    instructions = lines[0]

    nodes = {k: v for k, v in [process_line(x) for x in lines[2:]]}

    locations = [x for x in nodes.keys() if x[-1] == "A"]
    steps = [get_step_count(x, instructions, nodes) for x in locations]

    result = 1

    for step in steps:
        result = lcd(result, step)

    return result


if __name__ == "__main__":
    print(main())
