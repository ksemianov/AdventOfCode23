from dataclasses import dataclass
from typing import Optional
import numpy as np


EPS = 1e-6


@dataclass
class Coord4f:
    x: float
    y: float
    t1: float
    t2: float


# xt = x + dx * t
# yt = y + dy * t
@dataclass
class Line2d:
    x: int
    y: int
    dx: int
    dy: int

    def equations(self) -> tuple[np.array, np.array]:
        A = np.array([[1, 0, -self.dx], [0, 1, -self.dy]])
        b = np.array([self.x, self.y])
        return A, b


def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


def parse_line(line: str) -> Line2d:
    position_part, speed_part = line.split(" @ ")
    x, y, _ = (int(v) for v in position_part.split(", "))
    dx, dy, _ = (int(v) for v in speed_part.split(", "))
    return Line2d(x, y, dx, dy)


def intersect(line1: Line2d, line2: Line2d) -> Optional[Coord4f]:
    A1, b1 = line1.equations()
    A2, b2 = line2.equations()
    A = np.zeros((4, 4))
    A[0:2, 0:3] = A1
    A[2:4, 0:2] = A2[:, 0:2]
    A[2:4, 3] = A2[:, 2]
    b = np.concatenate([b1, b2], axis=0)
    solution, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    if rank != 4:
        # check if the solution is the only one (not parallel or same line)
        return None

    result = Coord4f(*solution)

    if not (result.t1 > 0 and result.t2 > 0):
        # check if the solution is at a positive time
        return None

    return result


def main():
    text = get_text()
    lines = [parse_line(line) for line in text.split("\n")]
    n = len(lines)

    def check_bounds(coord: Coord4f) -> bool:
        lower = 200000000000000
        upper = 400000000000000
        return lower <= coord.x <= upper and lower <= coord.y <= upper

    result = 0

    for i in range(n):
        for j in range(i + 1, n):
            line_a = lines[i]
            line_b = lines[j]

            intersection = intersect(line_a, line_b)
            if intersection and check_bounds(intersection):
                result += 1

    return result


if __name__ == "__main__":
    print(main())
