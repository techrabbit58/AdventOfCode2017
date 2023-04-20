# the test result shall be 3
from dataclasses import dataclass

LEFT = -1
RIGHT = 1


@dataclass(frozen=True)
class Rule:
    write: bool
    direction: int
    next_state: str


States = dict[bool, Rule]
Blueprint = dict[str, States]
Tape = set[int]


test_blueprint: Blueprint = {
    "A": {
        False: Rule(True, RIGHT, "B"),
        True: Rule(False, LEFT, "B"),
    },
    "B": {
        False: Rule(True, LEFT, "A"),
        True: Rule(True, RIGHT, "A"),
    },
}

puzzle_blueprint: Blueprint = {
    "A": {
        False: Rule(True, RIGHT, "B"),
        True: Rule(False, LEFT, "C"),
    },
    "B": {
        False: Rule(True, LEFT, "A"),
        True: Rule(True, RIGHT, "D"),
    },
    "C": {
        False: Rule(False, LEFT, "B"),
        True: Rule(False, LEFT, "E"),
    },
    "D": {
        False: Rule(True, RIGHT, "A"),
        True: Rule(False, RIGHT, "B"),
    },
    "E": {
        False: Rule(True, LEFT, "F"),
        True: Rule(True, LEFT, "C"),
    },
    "F": {
        False: Rule(True, RIGHT, "D"),
        True: Rule(True, RIGHT, "A"),
    },
}


def solve(blueprint: Blueprint, state: str, steps_to_go: int) -> int:
    tape: Tape = set()
    cursor = 0
    for step in range(steps_to_go):
        current_value = cursor in tape
        if blueprint[state][current_value].write:
            tape.add(cursor)
        else:
            tape.discard(cursor)
        cursor += blueprint[state][current_value].direction
        state = blueprint[state][current_value].next_state
    return len(tape)


if __name__ == '__main__':
    print("test:", "OK" if solve(blueprint=test_blueprint, state="A", steps_to_go=6) == 3 else "Fail!")
    print("solution:", solve(blueprint=puzzle_blueprint, state="A", steps_to_go=12_667_664), "(shall be 4769)")
