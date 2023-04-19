def cycle(n: int) -> int:
    return 2 * n - 2


def parse(puzzle: str) -> dict[int, int]:
    layers = {}
    with open(puzzle) as file:
        for line in file:
            layer, width = line.strip().split(': ')
            layers[int(layer)] = int(width)
    return layers


def main(puzzle: str, label: str, expected: tuple[int, int] | None = None) -> None:
    layers: dict[int, int] = parse(puzzle)
    severity = 0
    for layer, width in layers.items():
        if layer % cycle(width):
            continue
        severity += layer * width
    print(f'part 1 {label:.^8} = {severity}{(", shall be " + str(expected[0])) if expected else ""}')
    delay = 0
    while True:
        delay += 1
        caught = False
        for layer, width in layers.items():
            if (layer + delay) % cycle(width):
                continue
            caught = True
            break
        if not caught:
            break
    print(f'part 2 {label:.^8} = {delay}{(", shall be " + str(expected[1])) if expected else ""}')


if __name__ == '__main__':
    print("-" * 40)
    main(puzzle="test.txt", label="test", expected=(24, 10))
    print("-" * 40)
    main(puzzle="puzzle.txt", label="solution", expected=(1844, 3897604))
    print("=" * 40)
