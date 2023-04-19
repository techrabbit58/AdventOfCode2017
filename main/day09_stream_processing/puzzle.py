from typing import Callable


def solve(puzzle: str) -> tuple[int, int]:
    stack: list[Callable[[str], None]] = []
    garbage_count: int = 0
    depth: int = 0
    score: int = 0

    def ignore_one_symbol(_: str) -> None:
        nonlocal stack, handle
        handle = stack.pop()

    def eat_garbage(ch: str) -> None:
        nonlocal stack, handle, garbage_count
        if ch == "!":
            stack.append(handle)
            handle = ignore_one_symbol
        elif ch == ">":
            handle = stack.pop()
        else:
            garbage_count += 1

    def is_in_group(ch: str) -> None:
        nonlocal depth, score, stack, handle
        if ch == "!":
            stack.append(handle)
            handle = ignore_one_symbol
        elif ch == "<":
            stack.append(handle)
            handle = eat_garbage
        elif ch == "{":
            stack.append(handle)
            depth += 1
            handle = is_in_group
        elif ch == "}":
            score += depth
            depth -= 1
            handle = stack.pop()

    def is_stack_empty(ch: str) -> None:
        nonlocal depth, stack, handle
        if ch == "!":
            stack.append(handle)
            handle = ignore_one_symbol
        elif ch == "<":
            stack.append(handle)
            handle = eat_garbage
        elif ch == "{":
            stack.append(handle)
            depth += 1
            handle = is_in_group

    handle: Callable[[str], None] = is_stack_empty
    for symbol in puzzle:
        handle(symbol)

    return score, garbage_count


if __name__ == '__main__':
    print(f'Test with an empty input  gives: {solve("") == (0, 0)}')
    print(f'Test 1 with only garbage  gives: {solve("<random characters>") == (0, 17)}')
    print(f'Test 2 with only garbage  gives: {solve("<<<<>") == (0, 3)}')
    print(f'Test 3 with only garbage  gives: {solve("<{!>}>") == (0, 2)}')
    print(f'Test 4 with only garbage  gives: {solve("<!!>") == (0, 0)}')
    print(f'Test 5 with only garbage  gives: {solve("<!!!>>") == (0, 0)}')
    text = '<{o"i!q,<{i<q>'
    print(f'Test 6 with only garbage  gives: {solve(text) == (0, 10)}')
    print(f'Test with only one group  gives: {solve("{}") == (1, 0)}')
    print(f'Test 1 with nested groups gives: {solve("{{{}}}") == (6, 0)}')
    print(f'Test 2 with nested groups gives: {solve("{{}{}}") == (5, 0)}')
    print(f'Test 3 with nested groups gives: {solve("{{{},{},{{}}}}") == (16, 0)}')
    print(f'Test 4 with nested groups gives: {solve("{<q>,<q>,<q>,<q>}") == (1, 4)}')
    print(f'Test 5 with nested groups gives: {solve("{{<ab>},{<ab>},{<ab>},{<ab>}}") == (9, 8)}')
    print(f'Test 6 with nested groups gives: {solve("{{<!!>},{<!!>},{<!!>},{<!!>}}") == (9, 0)}')
    print(f'Test 7 with nested groups gives: {solve("{{<!>},{<!>},{<!>},{<>}}") == (3, 12)}')
    print(f'Test 8 with nested groups gives: {solve("{{<q!>},{<q!>},{<q!>},{<ab>}}") == (3, 17)}')
    print("---")
    with open("puzzle.txt") as file:
        text = file.read()
    part1solution, part2solution = solve(text)
    print(f'part 1 solution = {part1solution:<6} (OK if 12396)')
    print(f'part 2 solution = {part2solution:<6} (OK if 6346)')
    print("===")
