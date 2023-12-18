from dataclasses import dataclass
from typing import Optional


@dataclass
class Entity:
    cat: str
    number: int


@dataclass
class Range:
    src_start: int
    dst_start: int
    length: int

    def to_dst(self, number: int) -> Optional[int]:
        if self.src_start <= number < self.src_start + self.length:
            return number + self.dst_start - self.src_start


@dataclass
class Map:
    src_cat: str
    dst_cat: str
    ranges: list[Range]

    def to_dst(self, src: Entity) -> Optional[Entity]:
        if src.cat != self.src_cat:
            return None

        for i in self.ranges:
            dst = i.to_dst(src.number)
            if dst:
                return Entity(cat=self.dst_cat, number=dst)

        return Entity(cat=self.dst_cat, number=src.number)


def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


def parse_seeds(text: str) -> list[int]:
    return [int(x) for x in text.split(": ")[-1].split(" ")]


def parse_range(text: str) -> Range:
    x, y, z = [int(x) for x in text.split(" ")]
    return Range(src_start=y, dst_start=x, length=z)


def parse_map(text: str) -> Map:
    cat_part, data_part = text.split(" map:\n")
    src_cat, dst_cat = cat_part.split("-to-")
    lines = data_part.split("\n")
    ranges = [parse_range(x) for x in lines]
    return Map(src_cat=src_cat, dst_cat=dst_cat, ranges=ranges)


def lookup_location(entity: Entity, maps: list[Map]) -> Optional[Entity]:
    if entity.cat == "location":
        return entity

    for i in maps:
        dst = i.to_dst(entity)
        if dst:
            final = lookup_location(dst, maps)
            if final:
                return final


def main():
    text = get_text()

    parts = text.split("\n\n")

    seeds = parse_seeds(parts[0])
    maps = [parse_map(x) for x in parts[1:]]

    minimal = None

    for seed in seeds:
        entity = Entity(cat="seed", number=seed)
        location = lookup_location(entity, maps)
        if location is None:
            continue

        if minimal is None:
            minimal = location.number
        else:
            minimal = min(minimal, location.number)

    return minimal


if __name__ == "__main__":
    print(main())
