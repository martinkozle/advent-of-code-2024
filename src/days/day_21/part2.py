import sys
from collections.abc import Iterator, MutableMapping

from rich.console import Console
from rich.progress import track

from src.prep import run_with_prep
from src.print import eprint
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
    if dx > 0:
        directions.append(">" * abs(dx))
    if dy < 0:
        directions.append("^" * abs(dy))

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
        case "A", "<":
            return "V<<A"
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


def iter_strings_to_chars(strings: Iterator[str]) -> Iterator[str]:
    for string in strings:
        yield from string


type NestedIterator[T] = Iterator[NestedIterator | T]


def iter_nested_iterator_to_chars(nested_iter: NestedIterator[str]) -> Iterator[str]:
    for it in nested_iter:
        if isinstance(it, str):
            yield from it
        else:
            yield from iter_nested_iterator_to_chars(it)


class Solver:
    def __init__(self) -> None:
        # self.cache: LRU[tuple[str, str, int], list[str]] = LRU(size=10_000_000)
        self.cache: MutableMapping[tuple[str, str, int], list[str]] = {}
        self.single_cache: MutableMapping[tuple[str, str], str] = {}
        self.human_len_cache: MutableMapping[tuple[str, str], int] = {}

    def from_to_direction_key_directions_single(
        self,
        from_key: str,
        to_key: str,
    ) -> str:
        return self.single_cache.setdefault(
            (from_key, to_key),
            from_to_key_to_directions(from_key, to_key, DIRECTIONAL_KEYPAD),
        )

    def from_to_direction_key_directions(
        self,
        from_key: str,
        to_key: str,
        depth: int,
    ) -> Iterator[str]:
        if (from_key, to_key, depth) in self.cache:
            return iter(self.cache[from_key, to_key, depth])
        keys = self.from_to_direction_key_directions_single(from_key, to_key)
        if depth == 1:
            return iter(keys)
        key_pairs = group_key_pairs(iter(keys))
        out_keys = iter_nested_iterator_to_chars(
            (
                self.from_to_direction_key_directions(
                    from_key,
                    to_key,
                    depth - 1,
                )
                for from_key, to_key in key_pairs
            ),
        )
        if depth < 20:
            out_keys_list = list(out_keys)
            self.cache[from_key, to_key, depth] = out_keys_list
            eprint(len(self.cache))
            out_keys = iter(out_keys_list)
        return out_keys

    def numeric_keys_final_human_len(self, keys: str) -> int:
        robot_1_keys = keys_to_directions(keys, NUMERIC_KEYPAD)

        human_input_len = 0
        for from_key, to_key in track(
            group_key_pairs(iter(robot_1_keys)),
            total=len(robot_1_keys) - 1,
            console=Console(file=sys.stderr),
        ):
            if (from_key, to_key) not in self.human_len_cache:
                final_robot_keys = self.from_to_direction_key_directions(
                    from_key,
                    to_key,
                    depth=24,
                )
                self.human_len_cache[from_key, to_key] = sum(
                    len(
                        self.from_to_direction_key_directions_single(
                            final_from_key,
                            final_to_key,
                        ),
                    )
                    for final_from_key, final_to_key in group_key_pairs(
                        iter_strings_to_chars(final_robot_keys),
                    )
                )
            human_input_len += self.human_len_cache[from_key, to_key]
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
