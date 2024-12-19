from src.prep import run_with_prep
from src.timing import timing


class Solver:
    def __init__(self, towels: set[str]) -> None:
        self.towels = towels
        self.max_len_towel = max(map(len, self.towels))
        self.cache: dict[tuple[str, int], int] = {}

    def rec(self, design: str, start_ind: int = 0) -> int:
        if start_ind == len(design):
            return 1
        if (design, start_ind) in self.cache:
            return self.cache[design, start_ind]
        count = 0
        for towel_len in range(1, min(self.max_len_towel, len(design) - start_ind) + 1):
            towel = design[start_ind : start_ind + towel_len]
            if towel in self.towels:
                count += self.rec(design, start_ind + len(towel))
        self.cache[design, start_ind] = count
        return count


@timing
def main(inp: str) -> None:
    towels_str, _, *designs = inp.split("\n")
    towels = towels_str.split(", ")
    solver = Solver(set(towels))
    count = sum(solver.rec(design) for design in designs)
    print(count)


if __name__ == "__main__":
    run_with_prep(main)
