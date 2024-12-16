from collections import deque
from typing import Literal, get_args

from src.prep import run_with_prep
from src.timing import timing

Direction = Literal["^", ">", "v", "<"]

DIRECTION_MOVEMENT: dict[Direction, tuple[int, int]] = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}

State = tuple[tuple[int, int], Direction, int]


def rotate(direction: Direction, amount: int = 1) -> Direction:
    directions = get_args(Direction)
    ind = directions.index(direction)
    next_ind = (ind + amount) % 4
    return directions[next_ind]


def move(location: tuple[int, int], direction: Direction) -> tuple[int, int]:
    dy, dx = DIRECTION_MOVEMENT[direction]
    return location[0] + dy, location[1] + dx


@timing
def main(inp: str) -> None:
    grid = [list(row) for row in inp.split("\n")]
    size_y = len(grid)
    size_x = len(grid[0])
    py: int | None = None
    px: int | None = None
    for y in range(size_y):
        for x in range(size_x):
            if grid[y][x] == "S":
                py = y
                px = x
    if py is None or px is None:
        raise RuntimeError("Unexpected state")

    visited: dict[tuple[tuple[int, int], Direction], int] = {}
    q: deque[State] = deque()
    q.append(((py, px), ">", 0))
    best_score = 2**63 - 1
    while len(q) > 0:
        state = q.popleft()
        (y, x), direction, score = state
        if score >= best_score:
            continue
        if grid[y][x] == "E":
            best_score = min(best_score, score)
            continue
        visited_key = (y, x), direction
        if visited_key in visited and visited[visited_key] <= score:
            continue
        visited[visited_key] = score

        ny, nx = move((y, x), direction)
        if 0 <= ny < size_y and 0 <= nx < size_x and grid[ny][nx] != "#":
            q.append(((ny, nx), direction, score + 1))

        q.append(((y, x), rotate(direction, 1), score + 1000))
        q.append(((y, x), rotate(direction, -1), score + 1000))

    print(best_score)


if __name__ == "__main__":
    run_with_prep(main)
