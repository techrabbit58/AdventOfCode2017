from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class CubeCoordinate:
    q: int
    r: int
    s: int

    def next(self, direction: str) -> Self:
        result = {
            "n": lambda x: CubeCoordinate(x.q, x.r - 1, x.s + 1),
            "s": lambda x: CubeCoordinate(x.q, x.r + 1, x.s - 1),
            "nw": lambda x: CubeCoordinate(x.q - 1, x.r, x.s + 1),
            "se": lambda x: CubeCoordinate(x.q + 1, x.r, x.s - 1),
            "ne": lambda x: CubeCoordinate(x.q + 1, x.r - 1, x.s),
            "sw": lambda x: CubeCoordinate(x.q - 1, x.r + 1, x.s),
        }
        return result[direction](self)

    def abs(self) -> int:
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2


def solve(puzzle: str, label: str, expected: tuple[int, int] | None = None) -> None:
    path = [direction for direction in puzzle.strip().split(',')]
    node = CubeCoordinate(0, 0, 0)
    max_distance = 0
    for step in path:
        node = node.next(step)
        max_distance = max(max_distance, node.abs())
    print(f"part 1 {label:^.8} = {node.abs()}{('' if expected is None else ', shall be ' + str(expected[0]))}")
    print(f"part 2 {label:^.8} = {max_distance}{('' if expected is None else ', shall be ' + str(expected[1]))}")


def main() -> None:
    solve("ne,ne,ne", "test", (3, 3))
    solve("ne,ne,sw,sw", "test", (0, 2))
    solve("ne,ne,s,s", "test", (2, 2))
    solve("se,sw,se,sw,sw", "test", (3, 3))
    with open("puzzle.txt") as file:
        puzzle = file.read()
    solve(puzzle, "solution", (664, 1447))


if __name__ == '__main__':
    main()
