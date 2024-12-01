import sys

from src.timing import timing


@timing
def main(inp: str) -> None:
    numbers = [list(map(int, line.split())) for line in inp.split("\n")]
    numbers1 = sorted(num1 for num1, _ in numbers)
    numbers2 = sorted(num2 for _, num2 in numbers)
    print(sum(abs(num1 - num2) for num1, num2 in zip(numbers1, numbers2, strict=True)))


if __name__ == "__main__":
    sys.setrecursionlimit(2**31 - 1)
    sys.set_int_max_str_digits(2**31 - 1)
    main(sys.stdin.read().strip())
