from dataclasses import dataclass
from z3 import Int, Solver, sat


# xt = x + dx * t
# yt = y + dy * t
# zt = z + dz * t
@dataclass
class Line3d:
    x: int
    y: int
    z: int
    dx: int
    dy: int
    dz: int


def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


def parse_line(line: str) -> Line3d:
    position_part, speed_part = line.split(" @ ")
    x, y, z = (int(v) for v in position_part.split(", "))
    dx, dy, dz = (int(v) for v in speed_part.split(", "))
    return Line3d(x, y, z, dx, dy, dz)


def main():
    text = get_text()
    lines = [parse_line(line) for line in text.split("\n")]

    x = Int("x")
    y = Int("y")
    z = Int("z")
    dx = Int("dx")
    dy = Int("dy")
    dz = Int("dz")

    solver = Solver()

    for i in range(3):
        line = lines[i]
        ti = Int(f"t{i}")
        solver.add(ti > 0)
        solver.add(x + dx * ti == line.x + line.dx * ti)
        solver.add(y + dy * ti == line.y + line.dy * ti)
        solver.add(z + dz * ti == line.z + line.dz * ti)

    assert solver.check() == sat
    model = solver.model()

    result = model[x].as_long() + model[y].as_long() + model[z].as_long()
    return result


if __name__ == "__main__":
    print(main())
