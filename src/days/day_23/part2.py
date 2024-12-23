from typing import cast

from src.prep import run_with_prep
from src.timing import timing


def normalize_computers[T: tuple](computers: T) -> T:
    return cast(T, tuple(sorted(computers)))


class Solver:
    def __init__(self, connections_dict: dict[str, set[str]]) -> None:
        self.connections_dict = connections_dict
        self.cache: dict[tuple[str, ...], set[str]] = {}

    def find_maximum_size_clique(self, clique: set[str]) -> set[str]:
        normalized_clique = normalize_computers(tuple(clique))
        if normalized_clique in self.cache:
            return self.cache[normalized_clique]
        largest_clique = clique
        for new_c, connections in self.connections_dict.items():
            if all(c in connections for c in clique):
                new_clique = self.find_maximum_size_clique(
                    clique | {new_c},
                )
                if len(new_clique) > len(largest_clique):
                    largest_clique = new_clique
        self.cache[normalized_clique] = largest_clique
        return largest_clique


@timing
def main(inp: str) -> None:
    connection_pairs = [
        normalize_computers((row[:2], row[3:])) for row in inp.strip().split("\n")
    ]
    connections_dict: dict[str, set[str]] = {}

    for c1, c2 in connection_pairs:
        connections_dict.setdefault(c1, set()).add(c2)
        connections_dict.setdefault(c2, set()).add(c1)

    solver = Solver(connections_dict)
    largest_clique = max(
        (solver.find_maximum_size_clique({c}) for c in connections_dict),
        key=len,
    )
    print(",".join(normalize_computers(tuple(largest_clique))))


if __name__ == "__main__":
    run_with_prep(main)
