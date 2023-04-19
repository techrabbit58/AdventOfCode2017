from typing import Iterable

INITIAL: str = '.#./..#/###'


def rotate(square: str) -> str:
    """rotate a square by 90 degrees to the right"""
    rows = square.split('/')
    columns = [''] * len(rows)
    for i, row in enumerate(rows):
        columns[-1 - i] = row
    return '/'.join(''.join(triple) for triple in zip(*columns))


def flip(square: str) -> str:
    """flip a square horizontal"""
    rows = [reversed(row) for row in square.split('/')]
    return '/'.join(''.join(triple) for triple in zip(*rows))


def variants(square: str) -> Iterable[str]:
    """
    return an iterator that allows to go through all variant of a given
    square in turn, so that the variants can be used to match a
    rule's key. Iterates through 4 variants (4 x rotate) if the square
    has size 2, and through 8 variants (one flip, and then 4 mpre rotates)
    if the square has size 3
    """
    for _ in range(4):
        yield square
        square = rotate(square)
    if len(square) > 5:
        square = flip(square)
        for _ in range(4):
            square = rotate(square)
            yield square


def parse(puzzle) -> dict[str, str]:
    """
    parse the textual puzzle input to a dictionary of transformation rules,
    where each entry is of the form key -> value == '01/23' -> '012/345/678',
    or '123/456/789' -> '0123/4567/89ab/cdef', with a '.' at position k meaning
    'this pixel is set to 0' and a '#' meaning 'this pixel is set to 1'
    """
    rules: dict[str, str] = {}
    with open(puzzle) as file:
        for line in file.readlines():
            k, v = line.split(' => ')
            rules[k] = v
    return rules


def size_of(grid: str) -> int:
    """calculate the size of the given square, which is equal to the length of it's first row"""
    return grid.index('/')


def match_rule(rules: dict[str, str], square: str) -> str | None:
    """check all variants of the square: find the matching rule key and return its value"""
    for k in variants(square):
        if k in rules:
            return rules[k]
    raise ValueError(f'square {square} did not match any rule')


def part1(puzzle: str):
    rules = parse(puzzle)
    grid = INITIAL
    print(match_rule(rules, grid))
    print(match_rule(rules, '../.#'))


def main():
    part1('test1.txt')


if __name__ == '__main__':
    main()
