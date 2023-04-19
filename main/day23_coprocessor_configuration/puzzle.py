from collections import deque
from typing import Self


def get_value(op: str, registers: dict[str, int]) -> int:
    return registers[op] if op.isalpha() else int(op)


def parse(puzzle: str) -> list[list[str]]:
    with open(puzzle) as file:
        instructions: list[list[str]] = [line.strip().split() for line in file]
    return instructions


class Computer:
    registers: dict[str, int]
    instructions: list[list[str]]
    receive_buffer: deque[int]
    index: int
    partner: Self
    calls_to_mul: int

    def __init__(self, instructions: list[list[str]]) -> None:
        self.instructions = instructions
        self.registers: dict[str, int] = {}
        for reg in 'abcdefgh':
            self.registers[reg] = 0
        self.index = 0
        self.is_waiting = False
        self.messages = 0
        self.calls_to_mul = 0

    def set_register(self, reg: str, value: int) -> None:
        self.registers[reg] = value

    def tick(self) -> bool:
        instructions = self.instructions
        registers = self.registers
        if 0 <= self.index < len(instructions):
            offset = 1
            match instructions[self.index]:
                case 'set', target, source:
                    registers[target] = get_value(source, registers)
                case 'sub', target, source:
                    registers[target] -= get_value(source, registers)
                case 'mul', target, source:
                    registers[target] *= get_value(source, registers)
                    self.calls_to_mul += 1
                case 'jnz', ref, distance:
                    shall_jump = get_value(ref, registers) != 0
                    if shall_jump:
                        offset = get_value(distance, registers)
                case other:
                    print('unhandled: ' + str(other))
            self.index += offset
            return True
        else:
            return False


def main():

    # part 1
    computer = Computer(parse("puzzle.txt"))
    while computer.tick():
        pass
    print("part 1 solution =", computer.calls_to_mul, "<- shall be 5929")

    # part 2
    computer = Computer(parse("puzzle.txt"))
    computer.set_register("a", 1)
    print("run part2.py instead, because it is the result of the puzzle code analysis (manual disassembly)")
    while computer.tick():
        print(computer.index, computer.instructions[computer.index], computer.registers)
        input('?')


if __name__ == '__main__':
    main()
