import sys
from collections import Counter

from src.timing import timing


@timing
def main(inp: str) -> None:
    numbers = [list(map(int, line.split())) for line in inp.split("\n")]
    numbers1 = [num1 for num1, _ in numbers]
    numbers2 = Counter(num2 for _, num2 in numbers)
    print(sum(numbers2.get(num1, 0) * num1 for num1 in numbers1))


if __name__ == "__main__":
    sys.setrecursionlimit(2**31 - 1)
    sys.set_int_max_str_digits(2**31 - 1)
    main(sys.stdin.read().strip())
