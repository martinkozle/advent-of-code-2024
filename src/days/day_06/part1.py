from src.prep import run_with_prep
from src.timing import timing

DIRECTION_MOVEMENT: dict[str, tuple[int, int]] = {
    "^": (-1, 0),
    ">": (0, 1),
    "V": (1, 0),
    "<": (0, -1),
}
NEXT_DIRECTION: dict[str, str] = {"^": ">", ">": "V", "V": "<", "<": "^"}


@timing
def main(inp: str) -> None:
    patrol_map = [list(line) for line in inp.split("\n")]
    visited: set[tuple[int, int]] = set()

    size_y = len(patrol_map)
    size_x = len(patrol_map[0])

    guard_pos: tuple[int, int] = (0, 0)
    direction = "^"

    for y in range(size_y):
        for x in range(size_x):
            if patrol_map[y][x] == "^":
                guard_pos = y, x

    while 0 <= guard_pos[0] < size_y and 0 <= guard_pos[1] < size_x:
        visited.add(guard_pos)
        movement = DIRECTION_MOVEMENT[direction]
        new_pos = guard_pos[0] + movement[0], guard_pos[1] + movement[1]
        if not (0 <= new_pos[0] < size_y and 0 <= new_pos[1] < size_x):
            break
        if patrol_map[new_pos[0]][new_pos[1]] == "#":
            direction = NEXT_DIRECTION[direction]
        else:
            guard_pos = new_pos

    print(len(visited))


if __name__ == "__main__":
    run_with_prep(main)
