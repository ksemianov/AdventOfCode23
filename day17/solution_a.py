from dataclasses import dataclass, field
from enum import Enum
from queue import PriorityQueue


def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


@dataclass(frozen=True)
class Coord:
    i: int
    j: int


class Direction(str, Enum):
    left = "l"
    up = "u"
    right = "r"
    down = "d"

    def turn_left(self) -> "Direction":
        if self == Direction.left:
            return Direction.down
        elif self == Direction.up:
            return Direction.left
        elif self == Direction.right:
            return Direction.up
        elif self == Direction.down:
            return Direction.right

    def turn_right(self) -> "Direction":
        if self == Direction.left:
            return Direction.up
        elif self == Direction.up:
            return Direction.right
        elif self == Direction.right:
            return Direction.down
        elif self == Direction.down:
            return Direction.left

    def move(self, src: Coord) -> Coord:
        if self == Direction.left:
            return Coord(src.i, src.j - 1)
        elif self == Direction.up:
            return Coord(src.i - 1, src.j)
        elif self == Direction.right:
            return Coord(src.i, src.j + 1)
        elif self == Direction.down:
            return Coord(src.i + 1, src.j)


@dataclass(frozen=True)
class Item:
    coord: Coord
    direction: Direction
    consecutive: int


@dataclass(order=True)
class PrioritizedItem:
    heat_loss: int
    item: Item = field(compare=False)


def dijkstra(graph: list[str]) -> int:
    n_rows = len(graph)
    n_cols = len(graph[0])
    start_item = Item(coord=Coord(0, 0), direction=Direction.right, consecutive=0)

    queue: PriorityQueue[PrioritizedItem] = PriorityQueue()
    queue.put(PrioritizedItem(heat_loss=0, item=start_item))
    heat_losses: dict[Item, int] = {start_item: 0}

    while queue.qsize():
        cur = queue.get()
        cur_item = cur.item
        cur_heat_loss = heat_losses[cur_item]

        next_directions = [
            cur_item.direction.turn_left(),
            cur_item.direction.turn_right(),
        ]
        if cur_item.consecutive < 3:
            next_directions.append(cur_item.direction)

        for next_direction in next_directions:
            next_coord = next_direction.move(cur_item.coord)
            if not (0 <= next_coord.i < n_rows and 0 <= next_coord.j < n_cols):
                continue

            next_heat_loss = cur_heat_loss + int(graph[next_coord.i][next_coord.j])
            next_consecutive = (
                cur_item.consecutive + 1 if next_direction == cur_item.direction else 1
            )
            next_item = Item(
                coord=next_coord,
                direction=next_direction,
                consecutive=next_consecutive,
            )
            if next_item not in heat_losses or heat_losses[next_item] > next_heat_loss:
                heat_losses[next_item] = next_heat_loss
                queue.put(PrioritizedItem(heat_loss=next_heat_loss, item=next_item))

    best = None
    for item, heat_loss in heat_losses.items():
        if not (item.coord.i == n_rows - 1 and item.coord.j == n_cols - 1):
            continue

        if best is None or best > heat_loss:
            best = heat_loss

    return best


def main():
    text = get_text()
    lines = text.split("\n")

    result = dijkstra(lines)

    return result


if __name__ == "__main__":
    print(main())
