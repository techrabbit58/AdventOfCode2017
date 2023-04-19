def solution(puzzle: str) -> tuple[int, int]:
    history: dict[tuple[int, ...], int] = {}
    mem_banks = tuple(int(n) for n in puzzle.strip().split())
    length = len(mem_banks)
    history[mem_banks] = 0
    steps = 0

    def find_bank_with_most_blocks() -> tuple[int, int]:
        nonlocal mem_banks
        index_of_max = 0
        max_blocks = -1
        for index, blocks in enumerate(mem_banks):
            if blocks > max_blocks:
                max_blocks = blocks
                index_of_max = index
        return index_of_max, max_blocks

    def update_mem_banks(index: int, blocks: int) -> None:
        nonlocal mem_banks, steps
        next_mem = list(mem_banks)
        next_mem[index] = 0
        index = (index + 1) % length
        while blocks > 0:
            next_mem[index] += 1
            index = (index + 1) % length
            blocks -= 1
        mem_banks = tuple(next_mem)
        steps += 1

    while True:
        update_mem_banks(*find_bank_with_most_blocks())
        if mem_banks in history:
            break
        history[mem_banks] = steps
    return steps, steps - history[mem_banks]


def main(puzzle: str, text: str) -> None:
    steps, cycles = solution(puzzle)
    print(f"part 1 {text:^8} = {steps}")
    print(f"part 2 {text:^8} = {cycles}")


if __name__ == '__main__':
    main('0     2   7    0 ', "test")
    main('0	5	10	0	11	14	13	4	11	8	8	7	1	4	12	11', "solution")
