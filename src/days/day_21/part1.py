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
        for from_key, to_key in group_key_pairs(keys)
    )


def group_key_pairs(keys: str) -> list[tuple[str, str]]:
    return [("A", keys[0])] + [(keys[i - 1], keys[i]) for i in range(1, len(keys))]


def numeric_keys_to_final_human(keys: str) -> str:
    robot_1_keys = keys_to_directions(keys, NUMERIC_KEYPAD)
    robot_2_keys = keys_to_directions(robot_1_keys, DIRECTIONAL_KEYPAD)
    human_keys = keys_to_directions(robot_2_keys, DIRECTIONAL_KEYPAD)
    return human_keys


@timing
def main(inp: str) -> None:
    codes = inp.strip().split("\n")
    result = sum(
        len(numeric_keys_to_final_human(code)) * int(code[:-1]) for code in codes
    )
    print(result)


if __name__ == "__main__":
    run_with_prep(main)
