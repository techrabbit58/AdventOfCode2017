def read_input(filename: str) -> list[int]:
    with open(filename) as file:
        puzzle = [int(number) for number in file.readlines()]
    return puzzle


def part1(memory: list[int]) -> int:
    index, steps, length = 0, 0, len(memory)
    while index < length:
        offset = memory[index]
        memory[index] += 1
        index += offset
        steps += 1
    return steps


def part2(memory: list[int]) -> int:
    index, steps, length = 0, 0, len(memory)
    while index < length:
        offset = memory[index]
        memory[index] += 1 if offset < 3 else -1
        index += offset
        steps += 1
    return steps


def main():
    puzzle = read_input("puzzle.txt")
    print(f"part 1 solution = {part1(puzzle.copy())}")
    print(f"part 2 solution = {part2(puzzle)}")


if __name__ == '__main__':
    main()
