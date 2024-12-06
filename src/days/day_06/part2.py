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

    size_y = len(patrol_map)
    size_x = len(patrol_map[0])

    start_guard_pos: tuple[int, int] = (0, 0)

    for y in range(size_y):
        for x in range(size_x):
            if patrol_map[y][x] == "^":
                start_guard_pos = y, x

    direction = "^"
    initially_visited: set[tuple[int, int]] = set()
    guard_pos = start_guard_pos
    while 0 <= guard_pos[0] < size_y and 0 <= guard_pos[1] < size_x:
        initially_visited.add(guard_pos)
        movement = DIRECTION_MOVEMENT[direction]
        new_pos = guard_pos[0] + movement[0], guard_pos[1] + movement[1]
        if not (0 <= new_pos[0] < size_y and 0 <= new_pos[1] < size_x):
            break
        if patrol_map[new_pos[0]][new_pos[1]] == "#":
            direction = NEXT_DIRECTION[direction]
        else:
            guard_pos = new_pos

    count = 0

    for ob_y in range(size_y):
        for ob_x in range(size_x):
            if (
                (ob_y, ob_x) not in initially_visited
                or (ob_y, ob_x) == start_guard_pos
                or patrol_map[ob_y][ob_x] == "#"
            ):
                continue
            guard_pos = start_guard_pos
            direction = "^"
            visited_direction: set[tuple[int, int, str]] = set()
            while 0 <= guard_pos[0] < size_y and 0 <= guard_pos[1] < size_x:
                if (guard_pos[0], guard_pos[1], direction) in visited_direction:
                    count += 1
                    break
                visited_direction.add((guard_pos[0], guard_pos[1], direction))
                movement = DIRECTION_MOVEMENT[direction]
                new_pos = guard_pos[0] + movement[0], guard_pos[1] + movement[1]
                if not (0 <= new_pos[0] < size_y and 0 <= new_pos[1] < size_x):
                    break
                if patrol_map[new_pos[0]][new_pos[1]] == "#" or new_pos == (ob_y, ob_x):
                    direction = NEXT_DIRECTION[direction]
                else:
                    guard_pos = new_pos

    print(count)


if __name__ == "__main__":
    run_with_prep(main)
