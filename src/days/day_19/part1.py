from src.prep import run_with_prep
from src.timing import timing


class Solver:
    def __init__(self, towels: set[str]) -> None:
        self.towels = towels
        self.max_len_towel = max(map(len, self.towels))
        self.cache: dict[tuple[str, int], bool] = {}

    def rec(self, design: str, start_ind: int = 0) -> bool:
        if start_ind == len(design):
            return True
        if (design, start_ind) in self.cache:
            return self.cache[design, start_ind]
        for towel_len in range(1, self.max_len_towel + 1):
            towel = design[start_ind : start_ind + towel_len]
            if towel in self.towels:
                out = self.rec(design, start_ind + len(towel))
                if out:
                    self.cache[design, start_ind] = True
                    return True
        self.cache[design, start_ind] = False
        return False


@timing
def main(inp: str) -> None:
    towels_str, _, *designs = inp.split("\n")
    towels = towels_str.split(", ")
    solver = Solver(set(towels))
    count = sum(solver.rec(design) for design in designs)
    print(count)


if __name__ == "__main__":
    run_with_prep(main)
