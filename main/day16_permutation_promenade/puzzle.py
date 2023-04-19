from dataclasses import dataclass
from typing import Protocol


class Instruction(Protocol):
    def apply_to(self, programs: list[str]) -> list[str]:
        ...


@dataclass(frozen=True)
class Spin:
    length: int

    def apply_to(self, programs: list[str]) -> list[str]:
        return programs[-self.length:] + programs[:-self.length]


@dataclass(frozen=True)
class Exchange:
    a: int
    b: int

    def apply_to(self, programs: list[str]) -> list[str]:
        programs[self.a], programs[self.b] = programs[self.b], programs[self.a]
        return programs


@dataclass(frozen=True)
class Partner:
    a: str
    b: str

    def apply_to(self, programs: list[str]) -> list[str]:
        i, j = programs.index(self.a), programs.index(self.b)
        programs[i], programs[j] = programs[j], programs[i]
        return programs


def instruction_from_text(text: str) -> Instruction:
    if text[0] == 's':
        return Spin(int(text[1:]))
    elif text[0] == 'x':
        a, b = text[1:].split('/')
        return Exchange(int(a), int(b))
    elif text[0] == 'p':
        a, b = text[1:].split('/')
        return Partner(a, b)


def main(puzzle: str, programs: list[str], label: str, expected: tuple[str, str]):
    on_entry = programs.copy()
    with open(puzzle) as file:
        sequence = [instruction_from_text(line) for line in file.read().strip().split(',')]
    for instruction in sequence:
        programs = instruction.apply_to(programs)
    if label == 'test':
        print(f'part 1 {label:.^8} = {"".join(programs) == expected[0]}')
        for _ in range(1, 2):
            for instruction in sequence:
                programs = instruction.apply_to(programs)
        print(f'part 2 {label:.^8} = {"".join(programs) == expected[1]}')
    else:
        print(f'part 1 {label:.^8} = {"".join(programs)}, shall be {expected[0]}')
        total = 1
        while programs != on_entry:
            total += 1
            for instruction in sequence:
                programs = instruction.apply_to(programs)
        for _ in range(1_000_000_000 % total):
            for instruction in sequence:
                programs = instruction.apply_to(programs)
        print(f'part 2 {label:.^8} = {"".join(programs)}, shall be {expected[1]}')


if __name__ == '__main__':
    main(puzzle="test.txt",
         programs=list("abcde"), label="test",
         expected=('baedc', 'ceadb'))
    main(puzzle="puzzle.txt",
         programs=list("abcdefghijklmnop"), label="solution",
         expected=('namdgkbhifpceloj', 'ibmchklnofjpdeag'))
