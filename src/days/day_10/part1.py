from src.prep import run_with_prep
from src.timing import timing

DIRECTIONS: list[tuple[int, int]] = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Solver:
    def __init__(self, lines: list[str]) -> None:
        self.lines = lines
        self.cache: dict[tuple[int, int], set[tuple[int, int]]] = {}

    def rec_count(self, loc: tuple[int, int]) -> set[tuple[int, int]]:
        y, x = loc

        if loc in self.cache:
            return self.cache[loc]

        if self.lines[y][x] == "9":
            self.cache[loc] = {loc}
            return {loc}

        destinations: set[tuple[int, int]] = set()
        for dy, dx in DIRECTIONS:
            new_loc = (y + dy, x + dx)
            if (
                0 <= new_loc[0] < len(self.lines)
                and 0 <= new_loc[1] < len(self.lines[0])
                and int(self.lines[new_loc[0]][new_loc[1]]) == int(self.lines[y][x]) + 1
            ):
                destinations |= self.rec_count(new_loc)

        self.cache[loc] = destinations

        return destinations


@timing
def main(inp: str) -> None:
    lines = inp.split("\n")
    size_y = len(lines)
    size_x = len(lines[0])

    solver = Solver(lines=lines)
    counter = 0
    for y in range(size_x):
        for x in range(size_y):
            if lines[y][x] == "0":
                counter += len(solver.rec_count((y, x)))

    print(counter)


if __name__ == "__main__":
    run_with_prep(main)
