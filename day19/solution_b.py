from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import Optional

MIN = 1
MAX = 4000
RATING_IDENTIFIERS = ["x", "m", "a", "s"]


class ConditionSign(str, Enum):
    lt = "<"
    gt = ">"


@dataclass
class Condition:
    rating_identifier: str
    rating_value: int
    condition_sign: ConditionSign


@dataclass
class Interval:
    lower: int
    upper: int

    @property
    def length(self) -> int:
        return self.upper - self.lower + 1

    def __repr__(self) -> str:
        return f"[{self.lower}, {self.upper}]"


@dataclass
class Rule:
    condition: Optional[Condition]
    workflow: str

    def apply_single(self, interval: Interval) -> Optional[Interval]:
        if self.condition is None:
            return interval

        if self.condition.condition_sign == ConditionSign.lt:
            return intersect_single(
                interval, Interval(MIN, self.condition.rating_value - 1)
            )
        else:
            return intersect_single(
                interval, Interval(self.condition.rating_value + 1, MAX)
            )

    def apply(self, intervals: dict[str, Interval]) -> Optional[dict[str, Interval]]:
        if self.condition is None:
            return intervals

        mapped_interval = self.apply_single(intervals[self.condition.rating_identifier])
        if mapped_interval is None:
            return None

        intervals = deepcopy(intervals)
        intervals[self.condition.rating_identifier] = mapped_interval

        return intervals

    def negative_apply_single(self, interval: Interval) -> Optional[Interval]:
        if self.condition is None:
            return None

        if self.condition.condition_sign == ConditionSign.lt:
            return intersect_single(
                interval, Interval(self.condition.rating_value, MAX)
            )
        else:
            return intersect_single(
                interval, Interval(MIN, self.condition.rating_value)
            )

    def negative_apply(
        self, intervals: dict[str, Interval]
    ) -> Optional[dict[str, Interval]]:
        if self.condition is None:
            return None

        mapped_interval = self.negative_apply_single(
            intervals[self.condition.rating_identifier]
        )
        if mapped_interval is None:
            return None

        intervals = deepcopy(intervals)
        intervals[self.condition.rating_identifier] = mapped_interval

        return intervals


def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


def parse_rule(rule: str) -> Rule:
    if ConditionSign.lt in rule:
        condition_sign = ConditionSign.lt
    elif ConditionSign.gt in rule:
        condition_sign = ConditionSign.gt
    else:
        return Rule(workflow=rule, condition=None)

    condition_part, workflow = rule.split(":")
    rating_identifier, rating_value_part = condition_part.split(condition_sign)
    condition = Condition(
        rating_identifier=rating_identifier,
        rating_value=int(rating_value_part),
        condition_sign=condition_sign,
    )
    return Rule(workflow=workflow, condition=condition)


def parse_workflow_line(line: str) -> tuple[str, list[Rule]]:
    workflow, rules = line.strip("}").split("{")
    return workflow, [parse_rule(x) for x in rules.split(",")]


def parse_rating(rating: str) -> tuple[str, int]:
    rating_identifier, rating_value_part = rating.split("=")
    return rating_identifier, int(rating_value_part)


def parse_rating_line(line: str) -> dict[str, int]:
    return {k: v for k, v in (parse_rating(x) for x in line.strip("{}").split(","))}


def collect(
    intervals: dict[str, Interval], workflow: str, workflows: dict[str, list[Rule]]
) -> int:
    if workflow == "A":
        return count(intervals)
    elif workflow == "R":
        return 0

    intervals = deepcopy(intervals)

    result = 0
    rules = workflows[workflow]
    for rule in rules:
        new_intervals = rule.apply(intervals)
        if new_intervals:
            result += collect(new_intervals, rule.workflow, workflows)
            intervals = rule.negative_apply(intervals)

    return result


def intersect_single(interval1: Interval, interval2: Interval) -> Optional[Interval]:
    lower = max(interval1.lower, interval2.lower)
    upper = min(interval1.upper, interval2.upper)

    if lower > upper:
        return None

    return Interval(lower, upper)


def intersect(
    intervals1: dict[str, Interval], intervals2: dict[str, Interval]
) -> Optional[dict[str, Interval]]:
    new_intervals = {}

    for k in RATING_IDENTIFIERS:
        intersection = intersect_single(intervals1[k], intervals2[k])
        if not intersection:
            return None
        new_intervals[k] = intersection

    return new_intervals


def count(intervals: dict[str, Interval]) -> int:
    product = 1
    for interval in intervals.values():
        product *= interval.length
    return product


def main():
    text = get_text()
    workflows_part, _ = text.split("\n\n")
    workflows = {
        k: v for k, v in (parse_workflow_line(x) for x in workflows_part.split("\n"))
    }

    intervals = {k: Interval(MIN, MAX) for k in RATING_IDENTIFIERS}
    result = collect(intervals, "in", workflows)

    return result


if __name__ == "__main__":
    print(main())
