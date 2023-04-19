def parse(puzzle: str):
    with open(puzzle) as file:
        lines = [line.strip() for line in file.read().strip().split()]
    row_bias = -(len(lines) // 2)
    col_bias = -(len(lines[0]) // 2)
    infected = set()
    for row, single_line in enumerate(lines, row_bias):
        for col, symbol in enumerate(single_line, col_bias):
            if symbol == '#':
                infected.add((row, col))
    return infected


def part1(puzzle: str):
    infected = parse(puzzle)
    print(infected)


def main():
    part1("test.txt")


if __name__ == '__main__':
    main()
