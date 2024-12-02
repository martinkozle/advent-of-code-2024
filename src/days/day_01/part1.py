from src.parse import parse_line_ints
from src.prep import run_with_prep
from src.timing import timing


@timing
def main(inp: str) -> None:
    numbers = parse_line_ints(inp)
    numbers1 = sorted(num1 for num1, _ in numbers)
    numbers2 = sorted(num2 for _, num2 in numbers)
    print(sum(abs(num1 - num2) for num1, num2 in zip(numbers1, numbers2, strict=True)))


if __name__ == "__main__":
    run_with_prep(main)
