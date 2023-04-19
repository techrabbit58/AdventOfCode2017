from collections import Counter
from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class Triple:
    x: int
    y: int
    z: int

    @classmethod
    def from_str(cls, text: str) -> Self:
        _, x, y, z = text.replace('=<', ' ').replace('>', '').replace(',', ' ').split()
        return cls(int(x), int(y), int(z))

    def add(self, other: Self) -> Self:
        return Triple(self.x + other.x, self.y + other.y, self.z + other.z)


@dataclass
class Particle:
    position: Triple
    velocity: Triple
    acceleration: Triple

    @classmethod
    def from_str(cls, text: str) -> Self:
        p, v, a = text.split(', ')
        return cls(Triple.from_str(p), Triple.from_str(v), Triple.from_str(a))

    def distance_to_origin(self) -> int:
        return abs(self.position.x) + abs(self.position.y) + abs(self.position.z)

    def abs_acceleration(self) -> int:
        return abs(self.acceleration.x) + abs(self.acceleration.y) + abs(self.acceleration.z)


def find_slowest_particle(particles: list[Particle]) -> int:
    slowest_particle = 0
    min_acceleration = particles[0].abs_acceleration()
    for i, p in enumerate(particles):
        this_acceleration = p.abs_acceleration()
        if this_acceleration < min_acceleration:
            min_acceleration = this_acceleration
            slowest_particle = i
    return slowest_particle


def move(particles: list[Particle]) -> list[Particle]:
    for particle in particles:
        particle.velocity = particle.velocity.add(particle.acceleration)
        particle.position = particle.position.add(particle.velocity)
    return particles


def collide(particles: list[Particle]) -> list[Particle]:
    counts: Counter[Triple, int] = Counter()
    for particle in particles:
        counts[particle.position] += 1
    return [particle for particle in particles if counts[particle.position] == 1]


def main(puzzle: str, label: str, expected: tuple[int, ...]):

    # parse input
    with open(puzzle) as file:
        particles = [Particle.from_str(line) for line in file.read().strip().split('\n')]

    # perform part 1
    part1solution = find_slowest_particle(particles)
    if label == "test 1":
        print(f'part 1 ..test..: {"OK" if part1solution == expected[0] else "Failed"}')
    elif label == 'solution':
        print(f'part 1 solution = {part1solution}, shall be {expected[0]}')

    # perform part 2
    ticks = 100    # arbitrary large number of ticks: I hope it is enough.
    if label == 'test 2':
        for _ in range(ticks):
            particles = collide(move(particles))
        print(f'part 2 ..test..: {"OK" if len(particles) == expected[1] else "Failed"}')
    elif label == 'solution':
        for _ in range(ticks):
            particles = collide(move(particles))
        print(f'part 2 solution = {len(particles)}, shall be {expected[1]}')


if __name__ == '__main__':
    print('-' * 40)
    main("test1.txt", "test 1", (0, 1))
    main("test2.txt", "test 2", (0, 1))
    print('-' * 40)
    main("puzzle.txt", "solution", (91, 567))
    print('=' * 40)
