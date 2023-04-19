from collections import Counter


def part1(phrases: list[list[str]]) -> int:
    valid = len(phrases)
    for phrase in phrases:
        counted = Counter(phrase)
        if sum(counted.values()) > len(counted):
            valid -= 1
    return valid


def part2(phrases: list[list[str]]) -> int:
    valid = len(phrases)
    for phrase in phrases:
        equalized = [''.join(sorted(list(word))) for word in phrase]
        counted = Counter(equalized)
        if sum(counted.values()) > len(counted):
            valid -= 1
    return valid


if __name__ == '__main__':
    with open("puzzle.txt") as file:
        passphrases = [phrase.strip().split() for phrase in file.readlines()]
    print(f"part 1 solution = {part1(passphrases)}")
    print(f"part 2 solution = {part2(passphrases)}")
