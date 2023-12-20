from collections import deque
from dataclasses import dataclass
from enum import Enum
from functools import reduce
from typing import Any, Optional
from math import gcd


class ModuleType(str, Enum):
    broadcast = "broadcaster"
    flip_flop = "%"
    conjunction = "&"


class PulseType(str, Enum):
    low = "low"
    high = "high"


@dataclass
class Module:
    module_type: ModuleType
    memory: Any
    destinations: list[str]

    def process_pulse(
        self, identifier: Optional[str], pulse: PulseType
    ) -> Optional[PulseType]:
        if self.module_type == ModuleType.broadcast:
            return pulse
        elif self.module_type == ModuleType.flip_flop:
            if pulse == PulseType.high:
                return None
            else:
                is_on = bool(self.memory)
                self.memory = not is_on
                return PulseType.low if is_on else PulseType.high
        elif self.module_type == ModuleType.conjunction:
            self.memory[identifier] = pulse
            all_high = all(x == PulseType.high for x in self.memory.values())
            return PulseType.low if all_high else PulseType.high


def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


def parse_line(line: str) -> tuple[str, Module]:
    module_type_part, destinations_part = line.split(" -> ")
    destinations = destinations_part.split(", ")

    if "%" in module_type_part:
        return module_type_part[1:], Module(
            module_type=ModuleType.flip_flop, memory=False, destinations=destinations
        )
    elif "&" in module_type_part:
        return module_type_part[1:], Module(
            module_type=ModuleType.conjunction, memory={}, destinations=destinations
        )
    elif "broadcaster" in module_type_part:
        return ModuleType.broadcast.value, Module(
            module_type=ModuleType.broadcast, memory=None, destinations=destinations
        )
    else:
        raise ValueError(f"Cannot parse module type {module_type_part}")


def main():
    text = get_text()
    lines = text.split("\n")
    modules: dict[str, Module] = {k: v for k, v in (parse_line(line) for line in lines)}
    for identifier, module in modules.items():
        for destination in module.destinations:
            destination_module = modules.get(destination)
            if (
                destination_module
                and destination_module.module_type == ModuleType.conjunction
            ):
                destination_module.memory[identifier] = PulseType.low

    cycles = {}

    for button_press_index in range(1_000_000):
        q = deque([("button", ModuleType.broadcast.value, PulseType.low)])
        while q:
            src_identifier, cur_identifier, pulse_type = q.popleft()

            # print(f"{src_identifier} -{pulse_type}-> {cur_identifier}")

            cur_module = modules.get(cur_identifier)
            if cur_module is None:
                continue

            new_pulse = cur_module.process_pulse(src_identifier, pulse_type)

            # rx is conjunction from rz, lf, br and fk so need all of them to be high
            # find cycles in rz, lf, br and fk
            if (
                cur_identifier in {"rz", "lf", "br", "fk"}
                and new_pulse == PulseType.high
            ):
                if cur_identifier not in cycles:
                    cycles[cur_identifier] = button_press_index + 1
            if len(cycles) == 4:
                # cycles found
                deltas = list(cycles.values())
                lcm = reduce(lambda x, y: x * y, deltas) // gcd(*deltas)
                return lcm

            if new_pulse:
                for dst_identifier in cur_module.destinations:
                    if dst_identifier == "rx" and new_pulse == PulseType.low:
                        return button_press_index + 1
                    q.append((cur_identifier, dst_identifier, new_pulse))

    raise RuntimeError("Maximal iteration count reached")


if __name__ == "__main__":
    print(main())
