from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ConditionSign(str, Enum):
    lt = "<"
    gt = ">"


@dataclass
class Condition:
    rating_identifier: str
    rating_value: int
    condition_sign: ConditionSign


@dataclass
class Rule:
    condition: Optional[Condition]
    workflow: str

    def check(self, ratings: dict[str, int]) -> bool:
        if self.condition is None:
            return True

        required_value = self.condition.rating_value
        actual_value = ratings[self.condition.rating_identifier]
        sign = self.condition.condition_sign

        return eval(f"{actual_value} {sign} {required_value}")


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


def check(
    rating: dict[str, int], workflow: str, workflows: dict[str, list[Rule]]
) -> bool:
    if workflow == "A":
        return True
    elif workflow == "R":
        return False

    rules = workflows[workflow]
    for rule in rules:
        if rule.check(rating):
            return check(rating, rule.workflow, workflows)

    raise RuntimeError("No rules matched in workflow")


def main():
    text = get_text()
    workflows_part, ratings_part = text.split("\n\n")
    workflows = {
        k: v for k, v in (parse_workflow_line(x) for x in workflows_part.split("\n"))
    }
    ratings = [parse_rating_line(x) for x in ratings_part.split("\n")]

    result = 0

    for rating in ratings:
        if check(rating, "in", workflows):
            result += sum(rating.values())

    return result


if __name__ == "__main__":
    print(main())
