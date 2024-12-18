from collections import deque
from typing import cast

from src.prep import run_with_prep
from src.timing import timing

SIZE_X = 71
SIZE_Y = 71

DIRECTIONS: list[tuple[int, int]] = [(1, 0), (-1, 0), (0, 1), (0, -1)]

State = tuple[tuple[int, int], int]


def is_traversable(grid: list[list[str]]) -> bool:
    q: deque[State] = deque()
    visited: dict[tuple[int, int], int] = {}
    q.append(((0, 0), 0))
    while len(q) > 0:
        state = q.popleft()
        (y, x), distance = state
        if (y, x) == (SIZE_Y - 1, SIZE_X - 1):
            return True
        if (y, x) in visited and visited[y, x] <= distance:
            continue
        visited[y, x] = distance
        for dy, dx in DIRECTIONS:
            ny = y + dy
            nx = x + dx
            if 0 <= ny < SIZE_Y and 0 <= nx < SIZE_X and grid[ny][nx] != "#":
                q.append(((ny, nx), distance + 1))
    return False


@timing
def main(inp: str) -> None:
    falling_bytes = [
        cast(tuple[int, int], tuple(map(int, row.split(","))))
        for row in inp.split("\n")
    ]
    grid = [["."] * SIZE_X for _ in range(SIZE_Y)]
    for x, y in falling_bytes:
        grid[y][x] = "#"
        if not is_traversable(grid):
            print(f"{x},{y}")
            break


if __name__ == "__main__":
    run_with_prep(main)
