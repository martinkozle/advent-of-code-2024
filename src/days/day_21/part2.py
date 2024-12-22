import sys
from collections.abc import Iterator, MutableMapping

from rich.console import Console
from rich.progress import track

from src.prep import run_with_prep
from src.timing import timing

type Keypad = dict[str, tuple[int, int]]

NUMERIC_KEYPAD = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}
DIRECTIONAL_KEYPAD = {"^": (0, 1), "A": (0, 2), "<": (1, 0), "V": (1, 1), ">": (1, 2)}
SINGLE_DELTA_TO_DIRECTION = {(1, 0): "V", (0, 1): ">", (-1, 0): "^", (0, -1): "<"}


def delta_to_directions(delta: tuple[int, int]) -> str:
    dy, dx = delta
    directions: list[str] = []
    if dx < 0:
        directions.append("<" * abs(dx))
    if dy > 0:
        directions.append("V" * abs(dy))
    if dy < 0:
        directions.append("^" * abs(dy))
    if dx > 0:
        directions.append(">" * abs(dx))

    return "".join(directions) + "A"


def from_to_key_to_directions(
    from_key: str,
    to_key: str,
    keypad: Keypad,
) -> str:
    # edge cases
    match from_key, to_key:
        case "^", "<":
            return "V<A"
        case "<", "^":
            return ">^A"
        case "A", "<":
            return "V<<A"
        case "<", "A":
            return ">>^A"
        case "1", "0":
            return ">VA"
        case "1", "A":
            return ">>VA"
        case "4", "0":
            return ">VVA"
        case "4", "A":
            return ">>VVA"
        case "7", "0":
            return ">VVVA"
        case "7", "A":
            return ">>VVVA"
        case "0", "1":
            return "^<A"
        case "A", "1":
            return "^<<A"
        case "0", "4":
            return "^^<A"
        case "A", "4":
            return "^^<<A"
        case "0", "7":
            return "^^^<A"
        case "A", "7":
            return "^^^<<A"
    fy, fx = keypad[from_key]
    ty, tx = keypad[to_key]
    dy = ty - fy
    dx = tx - fx
    return delta_to_directions((dy, dx))


def keys_to_directions(keys: str, keypad: Keypad) -> str:
    return "".join(
        from_to_key_to_directions(from_key, to_key, keypad)
        for from_key, to_key in group_key_pairs(iter(keys))
    )


def group_key_pairs(keys: Iterator[str]) -> Iterator[tuple[str, str]]:
    prev = next(keys)
    yield ("A", prev)
    for key in keys:
        yield (prev, key)
        prev = key


class Solver:
    def __init__(self) -> None:
        # self.cache: LRU[tuple[str, str, int], list[str]] = LRU(size=10_000_000)
        self.cache: MutableMapping[tuple[str, str, int], list[str]] = {}
        self.single_cache: MutableMapping[tuple[str, str], str] = {}
        self.human_len_cache: MutableMapping[tuple[str, str, int], int] = {}

    def from_to_direction_key_human_len(
        self,
        from_key: str,
        to_key: str,
        depth: int,
    ) -> int:
        if (from_key, to_key, depth) not in self.human_len_cache:
            keys = from_to_key_to_directions(from_key, to_key, DIRECTIONAL_KEYPAD)
            if depth == 1:
                self.human_len_cache[from_key, to_key, depth] = len(keys)
                return len(keys)

            key_pairs = group_key_pairs(iter(keys))

            self.human_len_cache[from_key, to_key, depth] = sum(
                self.from_to_direction_key_human_len(
                    from_key,
                    to_key,
                    depth - 1,
                )
                for from_key, to_key in key_pairs
            )
        return self.human_len_cache[from_key, to_key, depth]

    def numeric_keys_final_human_len(self, keys: str) -> int:
        robot_1_keys = keys_to_directions(keys, NUMERIC_KEYPAD)

        human_input_len = 0
        for from_key, to_key in track(
            group_key_pairs(iter(robot_1_keys)),
            total=len(robot_1_keys) - 1,
            console=Console(file=sys.stderr),
        ):
            human_input_len += self.from_to_direction_key_human_len(
                from_key,
                to_key,
                depth=25,
            )
        return human_input_len


@timing
def main(inp: str) -> None:
    codes = inp.strip().split("\n")
    solver = Solver()
    result = sum(
        solver.numeric_keys_final_human_len(code) * int(code[:-1]) for code in codes
    )
    print(result)


if __name__ == "__main__":
    run_with_prep(main)
