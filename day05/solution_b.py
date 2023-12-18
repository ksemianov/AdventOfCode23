from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class Range:
    start: int
    length: int

    @property
    def end(self) -> int:
        return self.start + self.length - 1

    def intersection(self, other: "Range") -> Optional["Range"]:
        if other.end < self.start:
            return None

        if other.start > self.end:
            return None

        start = max(self.start, other.start)
        length = min(self.length, other.end - start + 1)

        return Range(start=start, length=length)

    def subtraction(self, other: list["Range"]) -> list["Range"]:
        other.sort(key=lambda x: x.start)

        result = []
        current_start = self.start

        for sub_range in other:
            if sub_range.end < current_start:
                continue

            if sub_range.start > self.end:
                break

            if sub_range.start > current_start:
                result.append(Range(current_start, sub_range.start - current_start))

            current_start = min(self.end, sub_range.end) + 1

        if current_start <= self.end:
            result.append(Range(current_start, self.end - current_start + 1))

        return result


@dataclass
class Entity:
    cat: str
    range: Range


@dataclass
class RangeMap:
    src: Range
    offset: int

    def to_dst(self, src: Range) -> Optional[Range]:
        intersection = src.intersection(self.src)
        if not intersection:
            return None

        return Range(start=intersection.start + self.offset, length=intersection.length)


@dataclass
class CatMap:
    src_cat: str
    dst_cat: str
    range_maps: list[RangeMap]

    def to_dst(self, src: Entity) -> list[Entity]:
        if src.cat != self.src_cat:
            return []

        src_ranges: list[Range] = []
        dst_ranges: list[Range] = []

        for range_map in self.range_maps:
            intersection = range_map.src.intersection(src.range)
            if intersection:
                dst_range = range_map.to_dst(intersection)
                src_ranges.append(intersection)
                dst_ranges.append(dst_range)

        result_ranges = dst_ranges + src.range.subtraction(src_ranges)

        return [Entity(cat=self.dst_cat, range=x) for x in result_ranges]


def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


def parse_seeds(text: str) -> list[Entity]:
    numbers = [int(x) for x in text.split(": ")[-1].split(" ")]
    n_pairs = len(numbers) // 2
    ranges = [
        Range(start=numbers[x * 2], length=numbers[x * 2 + 1]) for x in range(n_pairs)
    ]
    return [Entity(cat="seed", range=x) for x in ranges]


def parse_range_map(text: str) -> RangeMap:
    dst_start, src_start, length = [int(x) for x in text.split(" ")]
    src = Range(start=src_start, length=length)
    offset = dst_start - src_start
    return RangeMap(src=src, offset=offset)


def parse_cat_map(text: str) -> CatMap:
    cat_part, data_part = text.split(" map:\n")
    src_cat, dst_cat = cat_part.split("-to-")
    lines = data_part.split("\n")
    range_maps = [parse_range_map(x) for x in lines]
    return CatMap(src_cat=src_cat, dst_cat=dst_cat, range_maps=range_maps)


def flatten_comprehension(matrix: Iterable[Iterable[Entity]]) -> list[Entity]:
    return [item for row in matrix for item in row]


def lookup_locations(entity: Entity, cat_maps: list[CatMap]) -> list[Entity]:
    if entity.cat == "location":
        return [entity]

    for i in cat_maps:
        dst = i.to_dst(entity)
        if dst:
            final = flatten_comprehension(lookup_locations(x, cat_maps) for x in dst)
            if final:
                return final

    return []


def main():
    text = get_text()

    parts = text.split("\n\n")

    seeds = parse_seeds(parts[0])
    cat_maps = [parse_cat_map(x) for x in parts[1:]]

    minimal = None

    for seed in seeds:
        locations = lookup_locations(seed, cat_maps)

        for location in locations:
            value = location.range.start

            if minimal is None:
                minimal = value
            else:
                minimal = min(minimal, value)

    return minimal


if __name__ == "__main__":
    print(main())
