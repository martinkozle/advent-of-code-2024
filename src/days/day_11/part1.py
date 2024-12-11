from src.prep import run_with_prep
from src.timing import timing


class Solver:
    def __init__(self, max_depth: int) -> None:
        self.max_depth = max_depth
        self.cache: dict[tuple[int, int], int] = {}

    def rec(self, stone: int, depth: int) -> int:
        if depth == self.max_depth:
            return 1

        if (stone, depth) in self.cache:
            return self.cache[stone, depth]

        if stone == 0:
            res = self.rec(1, depth + 1)
        elif len(str(stone)) % 2 == 0:
            digits_str = str(stone)
            res = self.rec(
                int(digits_str[: len(digits_str) // 2] or "0"),
                depth + 1,
            ) + self.rec(
                int(digits_str[len(digits_str) // 2 :] or "0"),
                depth + 1,
            )
        else:
            res = self.rec(stone * 2024, depth + 1)

        self.cache[stone, depth] = res
        return res


@timing
def main(inp: str) -> None:
    stones = list(map(int, inp.split()))
    solver = Solver(max_depth=25)
    print(sum(solver.rec(stone, 0) for stone in stones))


if __name__ == "__main__":
    run_with_prep(main)
