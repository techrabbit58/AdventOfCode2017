DIRECTIONS = {
    'n': (-1, 0),
    'e': (0, 1),
    's': (1, 0),
    'w': (0, -1),
}


def start_position(grid: dict[tuple[int, int], str]) -> tuple[int, int] | None:
    for row, col in grid:
        if row == 0:
            return row, col
    return None


def advance(position: tuple[int, int], direction: tuple[int, int]) -> tuple[int, int] | None:
    return position[0] + direction[0], position[1] + direction[1]


def solve(puzzle: str) -> tuple[str, int]:
    grid: dict[tuple[int, int], str] = {}
    with open(puzzle) as file:
        for row, line in enumerate(file.read().split('\n')):
            for col, ch in enumerate(line):
                if ch != ' ':
                    grid[(row, col)] = ch
    direction = DIRECTIONS['s']
    position = start_position(grid)
    letters: str = ''
    steps = 0
    while direction and position in grid:
        steps += 1
        if grid[position] == '+':
            current_direction = direction
            direction = None
            for k, v in DIRECTIONS.items():
                if v[0] == current_direction[0] or v[1] == current_direction[1]:
                    continue
                if advance(position, v) in grid:
                    direction = DIRECTIONS[k]
                    break
        elif grid[position] in '|-':
            pass
        else:
            letters += grid[position]
        if direction:
            position = advance(position, direction)
    return letters, steps


def main():
    letters, steps = solve("test.txt")
    print(f'part 1 ..test..: {letters == "ABCDEF"}')
    print(f'part 2 ..test..: {steps == 38}')
    letters, steps = solve("puzzle.txt")
    print(f'part 1 solution = {letters}, shall be RUEDAHWKSM')
    print(f'part 2 solution = {steps}, shall be 17264')


if __name__ == '__main__':
    main()
