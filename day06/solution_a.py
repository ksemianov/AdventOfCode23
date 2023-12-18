import re


def get_lines() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def get_numbers(text: str) -> list[int]:
    return [int(x) for x in re.findall(r"(\d+)", text)]


def get_distance(hold_time: int, move_time: int) -> int:
    return hold_time * move_time


def get_ways_to_win(time: int, distance: int) -> int:
    result = 0

    for hold_time in range(time + 1):
        if get_distance(hold_time=hold_time, move_time=time - hold_time) > distance:
            result += 1

    return result


def main():
    time_line, distance_line = get_lines()

    times = get_numbers(time_line)
    distances = get_numbers(distance_line)

    n_races = len(times)
    assert len(distances) == n_races

    result = 1
    for i in range(n_races):
        result *= get_ways_to_win(times[i], distances[i])

    return result


if __name__ == "__main__":
    print(main())
