from typing import cast

from src.prep import run_with_prep
from src.timing import timing


def normalize_computers[T: tuple](computers: T) -> T:
    return cast(T, tuple(sorted(computers)))


@timing
def main(inp: str) -> None:
    connection_pairs = [
        normalize_computers((row[:2], row[3:])) for row in inp.strip().split("\n")
    ]
    connections_dict: dict[str, set[str]] = {}

    for c1, c2 in connection_pairs:
        connections_dict.setdefault(c1, set()).add(c2)
        connections_dict.setdefault(c2, set()).add(c1)

    tripplets: set[tuple[str, str, str]] = set()

    for c1, c2 in connection_pairs:
        for c3 in connections_dict[c1]:
            if c3 != c2 and c3 in connections_dict[c2]:
                tripplets.add(normalize_computers((c1, c2, c3)))

    count = sum(
        1 for c1, c2, c3 in tripplets if c1[0] == "t" or c2[0] == "t" or c3[0] == "t"
    )
    print(count)


if __name__ == "__main__":
    run_with_prep(main)
