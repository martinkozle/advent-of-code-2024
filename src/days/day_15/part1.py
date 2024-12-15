from typing import Literal, cast, get_args

from src.prep import run_with_prep
from src.timing import timing

Direction = Literal["^", ">", "v", "<"]

DIRECTION_MOVEMENT: dict[Direction, tuple[int, int]] = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def move_push(
    grid: list[list[str]],
    direction: Direction,
    location: tuple[int, int],
) -> bool:
    dy, dx = DIRECTION_MOVEMENT[direction]
    y, x = location
    ty, tx = y + dy, x + dx
    if grid[ty][tx] == "#":
        return False

    if grid[ty][tx] == "O":
        move_push(grid, direction, (ty, tx))

    if grid[ty][tx] == ".":
        grid[ty][tx] = grid[y][x]
        grid[y][x] = "."
        return True

    return False


@timing
def main(inp: str) -> None:
    grid_str, moves_str = inp.split("\n\n")
    grid = [list(row) for row in grid_str.strip().split("\n")]
    moves: list[Direction] = [
        cast(Direction, char)
        for row in moves_str.strip()
        for char in row
        if char in get_args(Direction)
    ]
    size_y = len(grid)
    size_x = len(grid[0])
    py: int | None = None
    px: int | None = None
    for y in range(size_y):
        for x in range(size_x):
            if grid[y][x] == "@":
                py = y
                px = x
    if py is None or px is None:
        raise RuntimeError("Unexpected state")

    for move in moves:
        if move_push(grid, move, (py, px)):
            dy, dx = DIRECTION_MOVEMENT[move]
            py += dy
            px += dx
    # eprint("\n".join("".join(row) for row in grid))

    gps_coordinates_sum = 0

    for y in range(size_y):
        for x in range(size_x):
            if grid[y][x] == "O":
                gps_coordinates_sum += y * 100 + x

    print(gps_coordinates_sum)


if __name__ == "__main__":
    run_with_prep(main)
