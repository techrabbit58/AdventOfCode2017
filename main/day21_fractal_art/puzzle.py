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
    return '/'.join(''.join(triple) for triple in rows)


def variants(square: str) -> Iterable[str]:
    """
    return an iterator that allows to go through all variant of a given
    square in turn, so that the variants can be used to match a
    rule's key. Iterates through 4 variants (4 x rotate) if the square
    has size 2, and through 8 variants (one flip, and then additional
    4 x rotate) if the square has size 3
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
            k, v = line.strip().split(' => ')
            rules[k] = v
    return rules


def size_of(grid: str) -> int:
    """calculate the size of the given square, which is equal to the length of it's first row"""
    return grid.index('/')


def match_rule(square: str, rules: dict[str, str]) -> str | None:
    """check all variants of the square: find the matching rule key and return its value"""
    for variant in variants(square):
        if variant in rules:
            return rules[variant]
    print(f'square {square} did not match any rule')
    raise RuntimeError()


def split(grid: str) -> tuple[list[str], int]:
    size = size_of(grid)
    divider = 2 if size % 2 == 0 else 3
    squares = []
    grid_rows = grid.split('/')
    for row in range(0, size, divider):
        for col in range(0, size, divider):
            single_square = []
            for offset in range(divider):
                single_square.append(grid_rows[row + offset][col:col + divider])
            squares.append('/'.join(single_square))
    return squares, size // divider


def combine(squares: list[str], width: int) -> str:
    """
    combine a list of squares back to a whole grid. Combine any
    squares_per_row squares to a new row. Return the combined
    grid as a single string
    """
    element_size = size_of(squares[0])
    grid_rows = [''] * (element_size * width)
    for pos, single_square in enumerate(squares):
        square_rows = single_square.split('/')
        for offset, square_row in enumerate(square_rows):
            grid_rows[offset + element_size * (pos // width)] += square_row
    return '/'.join(grid_rows)


def solve(puzzle: str, iterations: int) -> int:
    rules = parse(puzzle)
    grid = INITIAL
    for i in range(iterations):
        squares, width = split(grid)
        squares = [match_rule(sq, rules) for sq in squares]
        grid = combine(squares, width)
    return grid.count('#')


def main():
    print(f'part 1 ..test..: {"OK" if solve("test.txt", 2) == 12 else "Fail!"}')
    print(f'part 1 solution {solve("puzzle.txt", 5)}, shall be 205')
    print(f'part 2 solution {solve("puzzle.txt", 18)}, shall be 3389823')


if __name__ == '__main__':
    main()
