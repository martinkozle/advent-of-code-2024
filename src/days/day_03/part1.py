import re

from src.prep import run_with_prep
from src.timing import timing


@timing
def main(inp: str) -> None:
    matches: list[tuple[str, ...]] = re.findall(r"mul\((\d+),(\d+)\)", inp)
    result = sum(int(num1) * int(num2) for num1, num2 in matches)
    print(result)


if __name__ == "__main__":
    run_with_prep(main)
