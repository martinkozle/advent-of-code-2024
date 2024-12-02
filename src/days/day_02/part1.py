from src.parse import parse_line_ints
from src.prep import run_with_prep
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


@timing
def main(inp: str) -> None:
    numbers_list = parse_line_ints(inp)
    count = sum(map(check, numbers_list))
    print(count)


if __name__ == "__main__":
    run_with_prep(main)