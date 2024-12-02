import sys

from src.parse import parse_line_ints
from src.timing import timing


def check(numbers: list[int]) -> bool:
    dec = numbers[1] < numbers[0]
    for i in range(1, len(numbers)):
        if dec and numbers[i] >= numbers[i - 1]:
            return False
        if not dec and numbers[i] <= numbers[i - 1]:
            return False
        if abs(numbers[i] - numbers[i - 1]) > 3:
            return False
    return True


def check_tolerant(numbers: list[int]) -> bool:
    combinations = [numbers, numbers[:-1]] + [
        numbers[: i - 1] + numbers[i:] for i in range(1, len(numbers))
    ]
    return any(map(check, combinations))


@timing
def main(inp: str) -> None:
    numbers_list = parse_line_ints(inp)
    count = sum(map(check_tolerant, numbers_list))
    print(count)


if __name__ == "__main__":
    sys.setrecursionlimit(2**31 - 1)
    sys.set_int_max_str_digits(2**31 - 1)
    main(sys.stdin.read().strip())
