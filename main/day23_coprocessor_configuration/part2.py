import math


def is_prime(n: int) -> bool:
    for d in range(2, int(math.sqrt(n)) + 1):
        if n % d == 0:
            return False
    return True


def main():
    b, c = 107900, 124900
    h = 0
    while b <= c:
        if not is_prime(b):
            h += 1
        b += 17
    print("part 2 solution =", h, "<- shall be 907")


if __name__ == '__main__':
    main()
