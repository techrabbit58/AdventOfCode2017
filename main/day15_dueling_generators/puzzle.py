from typing import Self

PARAMETERS: dict[str, int] = {"A-factor": 16807, "A-mod": 4, "B-factor": 48271, "B-mod": 8}


class Generator:
    factor: int
    divider: int = 2147483647
    value: int
    module: int

    def __init__(self, factor: int) -> None:
        self.factor = factor

    def set_module(self, module: int) -> Self:
        self.module = module
        return self

    def seed(self, start: int) -> Self:
        self.value = start
        return self

    def next(self) -> int:
        self.value = self.value * self.factor % self.divider
        return self.value

    def next_with_mod(self) -> int:
        while True:
            self.value = self.value * self.factor % self.divider
            if self.value % self.module == 0:
                break
        return self.value


def main(start: dict[str, int], label: str, expected: tuple[int, int]) -> None:
    generator_a: Generator = Generator(PARAMETERS["A-factor"]).seed(start["A"])
    generator_b: Generator = Generator(PARAMETERS["B-factor"]).seed(start["B"])
    total_matches = 0
    for _ in range(40_000_000):
        if generator_a.next() & 0xffff == generator_b.next() & 0xffff:
            total_matches += 1
    if label == "test":
        print(f'part 1 {label:.^8} = {expected[0] == total_matches}')
    else:
        print(f'part 1 {label:.^8} = {total_matches}, shall be {expected[0]}')
    generator_a.seed(start["A"]).set_module(PARAMETERS["A-mod"])
    generator_b.seed(start["B"]).set_module(PARAMETERS["B-mod"])
    total_matches = 0
    for _ in range(5_000_000):
        if generator_a.next_with_mod() & 0xffff == generator_b.next_with_mod() & 0xffff:
            total_matches += 1
    if label == "test":
        print(f'part 2 {label:.^8} = {expected[1] == total_matches}')
    else:
        print(f'part 2 {label:.^8} = {total_matches}, shall be {expected[1]}')


if __name__ == '__main__':
    main(start={"A": 65, "B": 8921}, label="test", expected=(588, 309))
    main(start={"A": 116, "B": 299}, label="solution", expected=(569, 298))
