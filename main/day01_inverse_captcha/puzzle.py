def part1(captcha: list[str]) -> int:
    answer = 0
    captcha.append(captcha[0])
    for i in range(len(captcha) - 1):
        if captcha[i] == captcha[i + 1]:
            answer += int(captcha[i])
    return answer


def part2(captcha: list[str]) -> int:
    answer = 0
    length = len(captcha)
    i, j = 0, len(captcha) // 2
    captcha += captcha
    while i < length:
        if captcha[i] == captcha[j]:
            answer += int(captcha[i])
        i, j = i + 1, j + 1
    return answer


if __name__ == '__main__':
    with open("puzzle.txt") as file:
        text = file.read().strip()
    print(f'part 1 solution = {part1(list(text))}')
    print(f'part 2 solution = {part2(list(text))}')
