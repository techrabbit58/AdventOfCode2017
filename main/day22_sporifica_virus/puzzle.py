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

REVERT: dict[str, str] = {
    "up": "down",
    "left": "right",
    "down": "up",
    "right": "left",
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

    def smart_burst(self, weakened: set[Vector], infected: set[Vector], flagged: set[Vector]) -> None:
        pos = self.position
        if pos in weakened:
            # weakened node: does not change direction
            weakened.remove(pos)
            infected.add(pos)
            self.infection_count += 1
        elif pos in infected:
            self.heading = TURN_RIGHT[self.heading]
            infected.remove(pos)
            flagged.add(pos)
        elif pos in flagged:
            self.heading = REVERT[self.heading]
            flagged.remove(pos)
        else:
            self.heading = TURN_LEFT[self.heading]
            weakened.add(pos)
        self.position = Vector(
            self.position.row + DIRECTION[self.heading].row,
            self.position.col + DIRECTION[self.heading].col,
        )


def part1(puzzle: str) -> int:
    infected = parse(puzzle)
    carrier = Carrier(Vector(0, 0), "up")
    for _ in range(10_000):
        carrier.burst(infected)
    return carrier.infection_count


def part2(puzzle: str, bursts: int) -> int:
    infected = parse(puzzle)
    weakened: set[Vector] = set()
    flagged: set[Vector] = set()
    carrier = Carrier(Vector(0, 0), "up")
    for _ in range(bursts):
        carrier.smart_burst(weakened, infected, flagged)
    return carrier.infection_count


def main():
    print("part 1 test:", "OK" if part1("test.txt") == 5587 else "Fail!")
    print("part 2 test 1:", "OK" if part2("test.txt", 100) == 26 else "Fail!")
    print("part 2 test 2:", "OK" if part2("test.txt", 10_000_000) == 2511944 else "Fail!")
    print("part 1 solution =", part1("puzzle.txt"), "<- shall be 5538")
    print("part 2 solution =", part2("puzzle.txt", 10_000_000), "<- shall be 2511090")


if __name__ == '__main__':
    main()
