from collections import deque
from typing import Protocol

REPETITIONS: int = 2017


class CircularBuffer(Protocol):

    def insert(self, value: int) -> None:
        ...

    def get_value_after(self, value: int) -> int:
        ...


class FullBuffer:
    buffer: deque[int]
    steps: int
    position: int

    def __init__(self, steps: int) -> None:
        self.steps = steps
        self.buffer = deque([0])
        self.position = 0
        self.next_value = 1

    def insert(self, value: int) -> None:
        self.position = ((self.position + self.steps) % len(self.buffer)) + 1
        self.buffer.insert(self.position, value)

    def get_value_after(self, value: int) -> int:
        index = self.buffer.index(value)
        return self.buffer[index + 1]


class ShortedBuffer:
    steps: int
    buffer: int
    length: int
    position: int

    def __init__(self, steps: int) -> None:
        self.steps = steps
        self.length = 1
        self.position = 0

    def insert(self, value: int) -> None:
        self.position = ((self.position + self.steps) % self.length) + 1
        self.length = value + 1
        if self.position == 1:
            self.buffer = value

    def get_value_after(self, _: int) -> int:
        return self.buffer


def solve(buffer: CircularBuffer, repetitions: int, predecessor: int) -> int:
    for n in range(repetitions):
        buffer.insert(n + 1)
    return buffer.get_value_after(predecessor)


if __name__ == '__main__':
    print(f'test: {"OK" if solve(FullBuffer(3), 2017, 2017) == 638 else "FAIL!"}')
    print(f'part 1 solution = {solve(FullBuffer(301), 2017, 2017)}, shall be 1642')
    print(f'part 2 solution = {solve(ShortedBuffer(301), 50_000_000 - 1, 0)}, shall be 33601318')
