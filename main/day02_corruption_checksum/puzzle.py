def part1(numbers: list[list[int]]) -> int:
    answer = 0
    for row in numbers:
        answer += max(row) - min(row)
    return answer


def part2(numbers: list[list[int]]) -> int:
    answer = 0
    for row in numbers:
        r = sorted(row, reverse=True)
        for i, p in enumerate(r[:-1]):
            for q in r[i + 1:]:
                if p % q == 0:
                    answer += p // q
                    break
    return answer


if __name__ == '__main__':
    table: list[list[int]] = []
    with open("puzzle.txt") as file:
        for line in file.readlines():
            table.append([int(n) for n in line.strip().split()])
    print(f'part 1 solution = {part1(table)}')
    print(f'part 2 solution = {part2(table)}')
