from dataclasses import dataclass


@dataclass(frozen=True)
class Vector:
    row: int
    col: int


DIRECTION: dict[str, Vector] = {
    "up": Vector(-1, 0),
    "right": Vector(0, 1),
    "down": Vector(1, 0),
    "left": Vector(0, -1),
}

TURN_RIGHT: dict[str, str] = {
    "up": "right",
    "right": "down",
    "down": "left",
    "left": "up",
}

TURN_LEFT: dict[str, str] = {
    "up": "left",
    "left": "down",
    "down": "right",
    "right": "up",
}


def parse(puzzle: str) -> set[Vector]:
    with open(puzzle) as file:
        lines = [line.strip() for line in file.read().strip().split()]
    row_bias = -(len(lines) // 2)
    col_bias = -(len(lines[0]) // 2)
    infected = set()
    for row, single_line in enumerate(lines, row_bias):
        for col, symbol in enumerate(single_line, col_bias):
            if symbol == '#':
                infected.add(Vector(row, col))
    return infected


@dataclass
class Carrier:
    position: Vector
    heading: str
    infection_count: int = 0

    def burst(self, infected: set[Vector]) -> None:
        if self.position in infected:
            self.heading = TURN_RIGHT[self.heading]
            infected.remove(self.position)
        else:
            self.heading = TURN_LEFT[self.heading]
            infected.add(self.position)
            self.infection_count += 1
        self.position = Vector(
            self.position.row + DIRECTION[self.heading].row,
            self.position.col + DIRECTION[self.heading].col,
        )


def part1(puzzle: str):
    infected = parse(puzzle)
    carrier = Carrier(Vector(0, 0), "up")
    for _ in range(10000):
        carrier.burst(infected)
    print(carrier.infection_count)


def main():
    part1("test.txt")
    part1("puzzle.txt")


if __name__ == '__main__':
    main()
