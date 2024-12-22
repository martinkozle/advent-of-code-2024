from collections.abc import Iterator
from itertools import islice
from typing import cast

from more_itertools import windowed

from src.prep import run_with_prep
from src.timing import timing

MODULO = 16777216


def secret_number_iter(init_secret: int) -> Iterator[int]:
    secret = init_secret
    while True:
        yield secret
        secret ^= secret << 6
        secret %= MODULO
        secret ^= secret >> 5
        secret %= MODULO
        secret ^= secret << 11
        secret %= MODULO


@timing
def main(inp: str) -> None:
    init_secrets = list(map(int, inp.strip().split("\n")))
    first_visited_sequences: set[tuple[int, tuple[int, int, int, int]]] = set()
    sequence_sums: dict[tuple[int, int, int, int], int] = {}
    for i, init_secret in enumerate(init_secrets):
        for secrets_window in windowed(
            islice(secret_number_iter(init_secret), 2000),
            5,
        ):
            secrets_window = cast(tuple[int, ...], secrets_window)
            sequence = (
                secrets_window[1] % 10 - secrets_window[0] % 10,
                secrets_window[2] % 10 - secrets_window[1] % 10,
                secrets_window[3] % 10 - secrets_window[2] % 10,
                secrets_window[4] % 10 - secrets_window[3] % 10,
            )
            if (i, sequence) not in first_visited_sequences:
                first_visited_sequences.add((i, sequence))
                sequence_sums[sequence] = (
                    sequence_sums.get(sequence, 0) + secrets_window[-1] % 10
                )

    total = max(sequence_sums.values())
    print(total)


if __name__ == "__main__":
    run_with_prep(main)
