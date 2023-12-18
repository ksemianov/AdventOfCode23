import re
from typing import Callable


def get_lines() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def get_number(text: str) -> int:
    number = ""

    for fragment in re.findall(r"(\d+)", text):
        number += fragment

    return int(number)


def get_distance(hold_time: int, move_time: int) -> int:
    return hold_time * move_time


def bisect_left(low: int, high: int, func: Callable[[int], bool]) -> int:
    if high - low < 2:
        return low

    mid = (low + high) // 2

    if func(mid):
        return bisect_left(low, mid, func)
    else:
        return bisect_left(mid, high, func)


def get_ways_to_win(time: int, distance: int) -> int:
    optimal_hold = time // 2

    start = (
        bisect_left(0, optimal_hold, lambda x: get_distance(x, time - x) > distance) + 1
    )
    end = bisect_left(
        optimal_hold, time, lambda x: get_distance(x, time - x) < distance
    )

    return end - start + 1


def main():
    time_line, distance_line = get_lines()

    time = get_number(time_line)
    distance = get_number(distance_line)

    return get_ways_to_win(time, distance)


if __name__ == "__main__":
    print(main())
