from collections import deque
from typing import Iterable

from day10_knot_hash import knot_hash

ENCODER = dict(zip('0123456789abcdef', range(16)))


def encoded(h: str) -> str:
    result = []
    for ch in h:
        result += list(f'{ENCODER[ch]:04b}')
    return ''.join(result)


def make_grid(key: str) -> list[list[int]]:
    grid: list[list[int]] = []
    for row in range(128):
        text = f'{key}-{row}'
        encoded_text = encoded(knot_hash(text))
        grid.append([int(val) for val in encoded_text])
    return grid


def neighbors(row: int, col: int) -> Iterable[tuple[int, int]]:
    yield row - 1, col
    yield row, col + 1
    yield row + 1, col
    yield row, col - 1


def discover_region(grid: list[list[int]], row: int, col: int) -> int:
    if grid[row][col] != 1:
        return 0
    queue: deque[tuple[int, int]] = deque([(row, col)])
    while len(queue):
        this_row, this_col = queue.popleft()
        grid[this_row][this_col] = -1
        for neighbor_row, neighbor_col in neighbors(this_row, this_col):
            if neighbor_row < 0 or neighbor_row >= 128 or neighbor_col < 0 or neighbor_col >= 128:
                continue
            if grid[neighbor_row][neighbor_col] != 1:
                continue
            queue.append((neighbor_row, neighbor_col))
    return 1


def count_regions(grid: list[list[int]]) -> int:
    length = len(grid)
    regions_count = 0
    for row in range(length):
        for col in range(length):
            if grid[row][col] == 1:
                regions_count += discover_region(grid, row, col)
    return regions_count


def main(key: str, label: str, expected: tuple[int, int] | None = None) -> None:
    grid = make_grid(key)
    ones_count = sum(row.count(1) for row in grid)
    print(f'part 1 {label:.^8} = {ones_count}{(", shall be " + str(expected[0])) if expected else ""}')
    regions = count_regions(grid)
    print(f'part 2 {label:.^8} = {regions}{(", shall be " + str(expected[1])) if expected else ""}')


if __name__ == '__main__':
    print('-' * 40)
    main(key='flqrgnkx', label='test', expected=(8108, 1242))
    print('-' * 40)
    main(key='vbqugkhl', label='solution', expected=(8148, 1180))
    print('=' * 40)
