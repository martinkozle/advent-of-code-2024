from collections import Counter

from src.parse import parse_line_ints
from src.prep import run_with_prep
from src.timing import timing


@timing
def main(inp: str) -> None:
    numbers = parse_line_ints(inp)
    numbers1 = [num1 for num1, _ in numbers]
    numbers2 = Counter(num2 for _, num2 in numbers)
    print(sum(numbers2.get(num1, 0) * num1 for num1 in numbers1))


if __name__ == "__main__":
    run_with_prep(main)
