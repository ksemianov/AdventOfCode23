from dataclasses import dataclass
from enum import Enum


class Direction(str, Enum):
    left = "2"
    up = "3"
    right = "0"
    down = "1"


@dataclass
class Coord:
    i: int
    j: int


@dataclass
class Command:
    direction: Direction
    length: int

    def move(self, src: Coord) -> Coord:
        if self.direction == Direction.left:
            return Coord(src.i, src.j - self.length)
        elif self.direction == Direction.up:
            return Coord(src.i - self.length, src.j)
        elif self.direction == Direction.right:
            return Coord(src.i, src.j + self.length)
        elif self.direction == Direction.down:
            return Coord(src.i + self.length, src.j)


@dataclass
class Edge:
    src: Coord
    dst: Coord


def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


def parse_line(line: str) -> Command:
    _, _, part3 = line.split(" ")
    hexadecimal = part3.strip("#()")
    return Command(direction=Direction(hexadecimal[-1]), length=int(hexadecimal[:5], 16))


def triangle_area_2(c1: Coord, c2: Coord, c3: Coord) -> int:
    return (c2.i - c1.i) * (c3.j - c1.j) - (c2.j - c1.j) * (c3.i - c1.i)


def main():
    text = get_text()
    lines = text.split("\n")
    commands = [parse_line(x) for x in lines]

    area2 = 0
    start = Coord(0, 0)
    current = start
    edge_length = 0
    for command in commands:
        next_coord = command.move(current)
        edge = Edge(src=current, dst=next_coord)
        current = next_coord
        increment = triangle_area_2(edge.src, edge.dst, start)
        area2 += increment
        edge_length += command.length

    return (abs(area2) + edge_length) // 2 + 1


if __name__ == "__main__":
    print(main())
