import re

from tqdm import tqdm


def get_lines() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def count(pattern: str, groups: list[int], cache: dict) -> int:
    pattern = pattern.strip(".")

    key = (pattern, tuple(groups))
    if key in cache:
        return cache[key]

    if not groups:
        result = int(re.fullmatch(r"[.?]*", pattern) is not None)
        cache[key] = result
        return result

    group = groups[0]

    result = 0

    for start in range(0, len(pattern) - group + 1):
        end = start + group
        if start > 0 and pattern[start - 1] == "#":
            break
        if end < len(pattern) and pattern[end] == "#":
            continue
        if re.fullmatch(r"[#?]*", pattern[start:end]):
            res = count(pattern[end + 1:], groups[1:], cache)
            result += res

    cache[key] = result
    return result


def process_line(line: str) -> int:
    pattern, groups = line.split(" ")
    groups = [int(x) for x in groups.split(",")]

    pattern = "?".join([pattern for _ in range(5)])
    groups = [x for _ in range(5) for x in groups]

    result = count(pattern, groups, {})
    return result


def main():
    lines = [x.strip() for x in get_lines()]

    result = 0

    for line in tqdm(lines):
        result += process_line(line)

    return result


if __name__ == "__main__":
    print(main())
