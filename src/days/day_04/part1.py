from src.prep import run_with_prep
from src.timing import timing


@timing
def main(inp: str) -> None:
    lines = inp.split("\n")
    combinations: list[str] = []
    combinations += lines
    combinations += [line[::-1] for line in lines]
    verticals = ["".join(line[i] for line in lines) for i in range(len(lines[0]))]
    combinations += verticals
    combinations += [line[::-1] for line in verticals]
    expanded = [line + "$" * 1000 for line in lines] + ["$" * 1000 for _ in range(1000)]
    diagonals = [
        "".join(expanded[d][d + offset] for d in range(200)).strip("$")
        for offset in range(len(lines))
    ] + [
        "".join(expanded[d + offset][d] for d in range(200)).strip("$")
        for offset in range(1, len(lines))
    ]
    combinations += diagonals
    combinations += [line[::-1] for line in diagonals]
    other_diagonals = [
        "".join(
            expanded[d][len(lines[0]) - 1 - d - offset] for d in range(len(lines))
        ).strip("$")
        for offset in range(len(lines))
    ] + [
        "".join(
            expanded[d + offset][len(lines[0]) - 1 - d] for d in range(len(lines))
        ).strip("$")
        for offset in range(1, len(lines))
    ]
    combinations += other_diagonals
    combinations += [line[::-1] for line in other_diagonals]

    result = sum(combination.count("XMAS") for combination in combinations)
    print(result)


if __name__ == "__main__":
    run_with_prep(main)
