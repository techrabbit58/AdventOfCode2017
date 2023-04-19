def _single_pass(elements: list[int], lengths: list[int], position: int = 0, skip_size: int = 0) \
        -> tuple[int, int, int, list[int]]:
    list_size = len(elements)

    def twist(streak_length: int) -> None:
        nonlocal elements, list_size, position
        streak = reversed([elements[(position + index) % list_size] for index in range(streak_length)])
        for index, num in enumerate(streak):
            elements[(position + index) % list_size] = num

    for length in lengths:
        twist(length)
        position = (position + length + skip_size) % list_size
        skip_size += 1

    return elements[0] * elements[1], position, skip_size, elements


def knot_hash(text: str) -> str:
    chars = [ord(ch) for ch in text] + [int(num) for num in '17,31,73,47,23'.strip().replace(',', ' ').split()]
    position, skip_size = 0, 0
    sparse_hash = [int(num) for num in range(256)]
    for _ in range(64):
        _, position, skip_size, sparse_hash = _single_pass(
            elements=sparse_hash, lengths=chars, position=position, skip_size=skip_size)
    groups = [0] * 16
    for i in range(16):
        groups[i] = sparse_hash[16 * i]
        for j in range(1, 16):
            groups[i] ^= sparse_hash[16 * i + j]
    return ''.join(f"{i:02x}" for i in groups)
