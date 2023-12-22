from dataclasses import dataclass
from typing import Optional
import bisect


@dataclass
class Coord3:
    x: int
    y: int
    z: int


@dataclass
class Brick:
    first: Coord3
    second: Coord3

    def stack(self, another: "Brick") -> Optional["Brick"]:
        if (
            another.first.z <= self.second.z
            or another.second.x < self.first.x
            or another.first.x > self.second.x
            or another.second.y < self.first.y
            or another.first.y > self.second.y
        ):
            return None

        distance = another.first.z - self.second.z - 1

        first = Coord3(another.first.x, another.first.y, another.first.z - distance)
        second = Coord3(another.second.x, another.second.y, another.second.z - distance)
        return Brick(first, second)

    def stack_from_floor(self) -> "Brick":
        distance = self.first.z - 0 - 1
        first = Coord3(self.first.x, self.first.y, self.first.z - distance)
        second = Coord3(self.second.x, self.second.y, self.second.z - distance)
        return Brick(first, second)


def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


def parse_coord(line: str) -> Coord3:
    return Coord3(*(int(x) for x in line.split(",")))


def parse_line(line: str) -> Brick:
    coords = [parse_coord(x) for x in line.split("~")]
    return Brick(*coords)


def get_supports(bricks: list[Brick]) -> list[set[int]]:
    results = []

    n = len(bricks)
    for i in range(n):
        result = set()

        for j in range(i + 1, n):
            stack = bricks[j].stack(bricks[i])
            if stack and stack.first.z == bricks[i].first.z:
                result.add(j)

        results.append(result)

    return results


def stack_bricks(bricks: list[Brick]) -> list[Brick]:
    brick_lookup = sorted(bricks, key=lambda x: x.first.z)
    stacked_bricks = []

    for another in brick_lookup:
        for brick in stacked_bricks:
            stacked_brick = brick.stack(another)
            if stacked_brick:
                break
        else:
            stacked_brick = another.stack_from_floor()

        position = bisect.bisect_right(
            [-x.second.z for x in stacked_bricks], -stacked_brick.second.z
        )
        stacked_bricks = (
            stacked_bricks[:position] + [stacked_brick] + stacked_bricks[position:]
        )

    return stacked_bricks


def main():
    text = get_text()
    lines = text.split("\n")
    bricks = [parse_line(x) for x in lines]
    bricks = stack_bricks(bricks)
    supports = get_supports(bricks)

    result = 0

    for index in range(len(bricks)):
        bad_candidate = {index}
        if all(x != bad_candidate for x in supports):
            result += 1

    return result


if __name__ == "__main__":
    print(main())
