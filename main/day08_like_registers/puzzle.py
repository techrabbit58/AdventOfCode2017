from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Instruction:
    reg: str
    op: str
    val: int
    ref: str
    cond: str
    ref_val: int


def new_instruction(line: str) -> Instruction:
    reg, op, val, _, ref, cond, ref_val = line.strip().split()
    return Instruction(reg, op, int(val), ref, cond, int(ref_val))


class Computer:
    reg: dict[str, int]
    highest_ever: int

    def __init__(self) -> None:
        self.reg = defaultdict(lambda: 0)
        self.highest_ever = -2**64

    def inc(self, ins: Instruction) -> None:
        if self.is_applicable(ins):
            self.reg[ins.reg] += ins.val
        self.highest_ever = max(self.highest_ever, self.part1())

    def dec(self, ins: Instruction) -> None:
        if self.is_applicable(ins):
            self.reg[ins.reg] -= ins.val
        self.highest_ever = max(self.highest_ever, self.part1())

    def part1(self) -> int:
        return max(self.reg.values())

    def is_applicable(self, ins: Instruction) -> bool:
        key, val = ins.ref, ins.ref_val
        match ins.cond:
            case ">":
                return self.reg[key] > val
            case "<":
                return self.reg[key] < val
            case "==":
                return self.reg[key] == val
            case "<=":
                return self.reg[key] <= val
            case ">=":
                return self.reg[key] >= val
            case "!=":
                return self.reg[key] != val
            case _:
                raise RuntimeError()

    def apply(self, ins: Instruction) -> None:
        if ins.op == "inc":
            return self.inc(ins)
        else:
            return self.dec(ins)

    def part2(self) -> int:
        return self.highest_ever


def parse(filename: str) -> list[Instruction]:
    instructions = []
    with open(filename) as file:
        for line in file:
            instructions.append(new_instruction(line.strip()))
    return instructions


def main(puzzle: str, label: str) -> None:
    solution = Computer()
    for instruction in parse(puzzle):
        solution.apply(instruction)
    print(f"part 1 {label:.^8} = {solution.part1()}")
    print(f"part 2 {label:.^8} = {solution.part2()}")


if __name__ == '__main__':
    main("test.txt", "test")
    print("(The test shall give the results 1 and 10.)")
    main("puzzle.txt", "solution")
    print("(The puzzle shall give the results 3612 and 3818.)")
