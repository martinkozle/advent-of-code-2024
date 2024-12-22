from collections.abc import Iterator

from more_itertools import nth

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
    total = 0
    for init_secret in init_secrets:
        secret = nth(secret_number_iter(init_secret), 2000)
        if secret is None:
            raise RuntimeError("Unexpected state")
        total += secret
    print(total)


if __name__ == "__main__":
    run_with_prep(main)
