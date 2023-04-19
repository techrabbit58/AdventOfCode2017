from day10_knot_hash import _single_pass, knot_hash

if __name__ == '__main__':
    test_lengths = [int(num) for num in '3,4,1,5'.strip().replace(',', ' ').split()]
    print(f"part 1 ..test.. = {_single_pass(elements=[0, 1, 2, 3, 4], lengths=test_lengths)[0]}, shall be 12")

    puzzle = '70,66,255,2,48,0,54,48,80,141,244,254,160,108,1,41'

    puzzle_lengths = [int(num) for num in puzzle.strip().replace(',', ' ').split()]
    sp = _single_pass(elements=[int(n) for n in range(256)], lengths=puzzle_lengths)[0]
    print(f"part 1 solution = {sp}, shall be 7888")

    print("---")

    print(f"part 2 .test.1. = {knot_hash('') == 'a2582a3a0e66e6e86e3812dcb672a272'}")
    print(f"part 2 .test.2. = {knot_hash('AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd'}")
    print(f"part 2 .test.3. = {knot_hash('1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d'}")
    print(f"part 2 .test.4. = {knot_hash('1,2,4') == '63960835bcdc130f0b66d7ff4f6a5a8e'}")

    print(f"part 2 solution = {knot_hash(puzzle)}, shall be decdf7d377879877173b7f2fb131cf1b")

    print("---")
