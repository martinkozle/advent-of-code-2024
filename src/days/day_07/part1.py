from src.prep import run_with_prep
from src.timing import timing


def rec(result: int, values: list[int], curr: int, ind: int) -> bool:
    if ind == len(values):
        return result == curr

    return rec(
        result,
        values,
        curr + values[ind],
        ind + 1,
    ) or rec(
        result,
        values,
        curr * values[ind],
        ind + 1,
    )


def solve(result: int, values: list[int]) -> bool:
    return rec(result, values, values[0], 1)


@timing
def main(inp: str) -> None:
    count = 0
    for line in inp.split("\n"):
        result_str, values_str = line.split(":")
        result = int(result_str)
        values = list(map(int, values_str.split()))
        if solve(result, values):
            count += result
    print(count)


if __name__ == "__main__":
    run_with_prep(main)
