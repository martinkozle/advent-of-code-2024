import re

from src.prep import run_with_prep
from src.timing import timing


@timing
def main(inp: str) -> None:
    matches: list[tuple[str, ...]] = re.findall(
        r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))",
        inp,
    )
    flag = True
    result = 0
    for num1, num2, do, dont in matches:
        if len(dont):
            flag = False
        if len(do):
            flag = True
        if flag and len(num1) and len(num2):
            result += int(num1) * int(num2)
    print(result)


if __name__ == "__main__":
    run_with_prep(main)
