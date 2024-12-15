from typing import Literal, cast, get_args

from src.prep import run_with_prep
from src.timing import timing

Direction = Literal["^", ">", "v", "<"]

GRID_MAPPING: dict[str, str] = {"#": "##", "O": "[]", ".": "..", "@": "@."}

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
    dry_run: bool = False,
) -> bool:
    dy, dx = DIRECTION_MOVEMENT[direction]
    y, x = location
    sources = [(y, x)]
    targets = [(y + dy, x + dx)]
    if grid[y][x] == "[" and direction in "^v":
        sources.append((y, x + 1))
        targets.append((y + dy, x + dx + 1))
    elif grid[y][x] == "]" and direction in "^v":
        sources.append((y, x - 1))
        targets.append((y + dy, x + dx - 1))

    if any(grid[ty][tx] == "#" for ty, tx in targets):
        return False

    if all(
        grid[ty][tx] == "."
        or (grid[ty][tx] in "[]" and move_push(grid, direction, (ty, tx), dry_run=True))
        for ty, tx in targets
    ):
        for ty, tx in targets:
            if grid[ty][tx] in "[]":
                move_push(grid, direction, (ty, tx), dry_run=dry_run)

        if not dry_run:
            for (sy, sx), (ty, tx) in zip(sources, targets, strict=False):
                grid[ty][tx] = grid[sy][sx]
                grid[sy][sx] = "."

        return True

    return False


@timing
def main(inp: str) -> None:
    grid_str, moves_str = inp.split("\n\n")
    grid = [
        [mapped_char for char in row for mapped_char in GRID_MAPPING[char]]
        for row in grid_str.strip().split("\n")
    ]
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
            if grid[y][x] == "[":
                gps_coordinates_sum += y * 100 + x

    print(gps_coordinates_sum)


if __name__ == "__main__":
    run_with_prep(main)
