from dataclasses import dataclass
from functools import cmp_to_key


HAND_SIZE: int = 5
CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
CARD_RANK = {x: i + 1 for i, x in enumerate(reversed(CARDS))}


@dataclass
class Line:
    hand: str
    hand_type: int
    bid: int


def get_lines() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def get_hand_type(hand: str) -> int:
    if all(hand[0] == x for x in hand):
        return 7

    for x in hand:
        if sum(y == x for y in hand) == 4:
            return 6

    if len(set(hand)) == 2:
        return 5

    for x in hand:
        if sum(y == x for y in hand) == 3:
            return 4

    if len(set(hand)) == 3:
        return 3

    if len(set(hand)) == 4:
        return 2

    return 1


def process_line(line: str) -> Line:
    hand, bid = line.split(" ")
    assert len(hand) == HAND_SIZE
    return Line(hand, get_hand_type(hand), int(bid))


def compare(line_a: Line, line_b: Line) -> int:
    hand_type_a = line_a.hand_type
    hand_type_b = line_b.hand_type

    if hand_type_a != hand_type_b:
        return -1 if hand_type_a < hand_type_b else 1

    hand_a = line_a.hand
    hand_b = line_b.hand

    for i in range(HAND_SIZE):
        card_rank_a = CARD_RANK[hand_a[i]]
        card_rank_b = CARD_RANK[hand_b[i]]
        if card_rank_a != card_rank_b:
            return -1 if card_rank_a < card_rank_b else 1

    return 0


def main():
    lines = [process_line(x) for x in get_lines()]

    lines.sort(key=cmp_to_key(compare))

    result = 0

    for i, line in enumerate(lines):
        result += (i + 1) * line.bid

    return result


if __name__ == "__main__":
    print(main())
