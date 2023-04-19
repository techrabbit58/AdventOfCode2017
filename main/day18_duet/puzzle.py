from collections import defaultdict, deque
from typing import Self


def value(op: str, registers: dict[str, int]) -> int:
    return registers[op] if op.isalpha() else int(op)


def part1(puzzle: str) -> int:
    with open(puzzle) as file:
        instructions: list[list[str]] = [line.strip().split() for line in file]
    registers: dict[str, int] = defaultdict(lambda: 0)
    sound_stack: int = 0
    index = 0
    while 0 <= index < len(instructions):
        offset = 1
        match instructions[index]:
            case 'snd', frequency:
                sound_stack = value(frequency, registers)
            case 'set', target, source:
                registers[target] = value(source, registers)
            case 'add', target, source:
                registers[target] += value(source, registers)
            case 'mul', target, source:
                registers[target] *= value(source, registers)
            case 'mod', target, source:
                registers[target] %= value(source, registers)
            case 'rcv', ref:
                shall_recover = value(ref, registers) != 0
                if shall_recover:
                    return sound_stack
            case 'jgz', ref, distance:
                shall_jump = value(ref, registers) > 0
                if shall_jump:
                    offset = value(distance, registers)
            case other:
                print('unhandled: ' + str(other))
        index += offset
    return -1


class Program:
    registers: dict[str, int]
    instructions: list[list[str]]
    receive_buffer: deque[int]
    index: int
    partner: Self
    is_waiting: bool
    messages: int

    def __init__(self, program_number: int, instructions: list[list[str]]) -> None:
        self.registers = defaultdict(lambda: 0)
        self.registers['p'] = program_number
        self.instructions = instructions
        self.receive_buffer = deque()
        self.index = 0
        self.is_waiting = False
        self.messages = 0

    def set_partner(self, partner: Self) -> None:
        self.partner = partner

    def accept(self, message: int) -> None:
        self.receive_buffer.append(message)

    def tick(self) -> bool:
        instructions = self.instructions
        registers = self.registers
        if 0 <= self.index < len(instructions):
            offset = 1
            match instructions[self.index]:
                case 'snd', message:
                    self.partner.accept(value(message, registers))
                    self.messages += 1
                case 'set', target, source:
                    registers[target] = value(source, registers)
                case 'add', target, source:
                    registers[target] += value(source, registers)
                case 'mul', target, source:
                    registers[target] *= value(source, registers)
                case 'mod', target, source:
                    registers[target] %= value(source, registers)
                case 'rcv', register:
                    if len(self.receive_buffer):
                        self.is_waiting = False
                        registers[register] = self.receive_buffer.popleft()
                    elif self.is_waiting and self.partner.is_waiting:
                        return True
                    else:
                        self.is_waiting = True
                        offset = 0
                case 'jgz', ref, distance:
                    shall_jump = value(ref, registers) > 0
                    if shall_jump:
                        offset = value(distance, registers)
                case other:
                    print('unhandled: ' + str(other))
            self.index += offset
            return False
        else:
            return True


def part2(puzzle) -> int:
    with open(puzzle) as file:
        instructions: list[list[str]] = [line.strip().split() for line in file]
    p0 = Program(0, instructions)
    p1 = Program(1, instructions)
    p0.set_partner(p1)
    p1.set_partner(p0)
    while True:
        a = p0.tick()
        b = p1.tick()
        if a and b:
            break
    return p1.messages


if __name__ == '__main__':
    print(f'part 1 test: {part1("test1.txt") == 4}')
    print(f'part 1 solution = {part1("puzzle.txt")}, shall be 3423')
    print(f'part 1 test: {part2("test2.txt") == 3}')
    print(f'part 2 solution = {part2("puzzle.txt")}, shall be 7493')
