from dataclasses import dataclass


@dataclass
class Component:
    a: int
    b: int


def part1(puzzle: str):
    with open(puzzle) as file:
        components = sorted((Component(*line.strip().split('/')) for line in file), key=lambda x: x.a)
    print(components)


def main():
    part1('puzzle.txt')


if __name__ == '__main__':
    main()
