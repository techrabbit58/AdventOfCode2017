from dataclasses import dataclass
from typing import Self


@dataclass
class Component:
    a: int
    b: int

    @classmethod
    def from_str(cls, text: str) -> Self:
        a, b = (int(x) for x in text.strip().split('/'))
        return Component(b, a) if a > b else Component(a, b)


def part1(puzzle: str):
    with open(puzzle) as file:
        components = sorted((Component.from_str(line) for line in file), key=lambda x: x.a)
    print(components)


def main():
    part1('test.txt')


if __name__ == '__main__':
    main()
