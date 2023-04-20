from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class Component:
    a: int
    b: int

    @classmethod
    def from_str(cls, text: str) -> Self:
        a, b = (int(x) for x in text.strip().split('/'))
        return Component(a, b)

    def strength(self) -> int:
        return self.a + self.b


ComponentSet = set[Component]


def parse(puzzle: str) -> ComponentSet:
    with open(puzzle) as file:
        components = {Component.from_str(line) for line in file}
    return components


def find_maximum_strength(anchor: int, components: ComponentSet) -> int:
    """
    find the strength of  with maximum strength by checking all possible bridges (depth first)
    """
    maximum_strength = 0
    for component in [c for c in components if c.a == anchor or c.b == anchor]:
        components.remove(component)
        strength = component.strength() \
            + find_maximum_strength(component.b if component.a == anchor else component.a, components)
        maximum_strength = max(maximum_strength, strength)
        components.add(component)
    return maximum_strength


def find_longest_bridge(anchor: int, components: ComponentSet) -> tuple[int, int]:
    """
    find the strength of the bridge with the longest number of components (aka. the longest bridge)
    """
    maximum_length = 0
    maximum_strength = 0
    for component in [c for c in components if c.a == anchor or c.b == anchor]:
        components.remove(component)
        length, strength = find_longest_bridge(component.b if component.a == anchor else component.a, components)
        strength += component.strength()
        length += 1
        if length == maximum_length:
            maximum_strength = max(maximum_strength, strength)
        elif length > maximum_length:
            maximum_length = length
            maximum_strength = strength
        components.add(component)
    return maximum_length, maximum_strength


def solve(puzzle: str, label: str, expected: str | int | None = None):
    components = parse(puzzle)
    if label == 'part 1 test':
        print(label, '=', "OK" if find_maximum_strength(0, components) == expected else "Fail!")
    elif label == "part 1 solution":
        print(label, '=',  find_maximum_strength(0, components), expected)
    elif label == 'part 2 test':
        print(label, '=', "OK" if find_longest_bridge(0, components)[1] == expected else "Fail!")
    elif label == 'part 2 solution':
        print(label, '=', find_longest_bridge(0, components)[1], expected)
    else:
        print("What?!")


def main():
    solve('test.txt', label='part 1 test', expected=31)
    solve('puzzle.txt', label='part 1 solution', expected="(shall be 1940)")
    solve('test.txt', label='part 2 test', expected=19)
    solve('puzzle.txt', label='part 2 solution', expected="(shall be 1928)")


if __name__ == '__main__':
    main()
