from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class ProgInfo:
    weight: int
    subs: list[str]


def get_puzzle_input(puzzle: str) -> dict[str, ProgInfo]:
    programs: dict[str, ProgInfo] = {}
    with open(puzzle) as file:
        for prog in file.readlines():
            head, weight, *tail = prog.strip().replace(", ", " ").split()
            programs[head] = ProgInfo(int(weight[1:-1]), [] if not len(tail) else tail[1:])
    return programs


def find_root(programs: dict[str, ProgInfo]) -> str:
    inventory: set[str] = set()
    dependents: set[str] = set()
    for prog, info in programs.items():
        inventory.add(prog)
        dependents.update(info.subs)
    return list(inventory.difference(dependents))[0]


def main(puzzle: str, text: str):
    programs_tree = get_puzzle_input(puzzle)
    root = find_root(programs_tree)
    print(f'part 1 {text:^8} = {root}')

    @lru_cache
    def get_branch_weight(prog: str) -> int:
        nonlocal programs_tree
        this_prog = programs_tree[prog]
        if len(this_prog.subs):
            weight = this_prog.weight + sum(get_branch_weight(p) for p in this_prog.subs)
        else:
            weight = programs_tree[prog].weight
        return weight

    def dfs_to_next_unbalanced_node(prog: str) -> tuple[str, int]:
        nonlocal programs_tree
        weights: dict[int, list[str]] = defaultdict(list)
        for sub in programs_tree[prog].subs:
            weights[get_branch_weight(sub)].append(sub)
        bad_weight, good_weight = 0, 0
        bad_prog = ""
        for weight, subs in weights.items():
            if len(subs) == 1:
                bad_prog = subs[0]
                bad_weight = weight
            else:
                good_weight = weight
        delta = good_weight - bad_weight
        return bad_prog, delta

    def find_bad_sub_and_delta(sub: str) -> tuple[str, int]:
        bad_branch = []
        prog, weight = dfs_to_next_unbalanced_node(sub)
        while prog != "":
            bad_branch.append((prog, weight))
            prog, weight = dfs_to_next_unbalanced_node(prog)
        return bad_branch[-1]

    s, d = find_bad_sub_and_delta(root)
    print(f"part 2 {text:^8} = {programs_tree[s].weight + d}")


if __name__ == '__main__':
    main("test.txt", "test")
    print("--- test should return 'tknk' and 60 ---")
    main("puzzle.txt", "solution")
