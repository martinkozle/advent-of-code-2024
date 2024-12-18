from collections import deque
from typing import cast

from src.prep import run_with_prep
from src.timing import timing

SIZE_X = 71
SIZE_Y = 71
FALLEN_MEMORY = 1024

DIRECTIONS: list[tuple[int, int]] = [(1, 0), (-1, 0), (0, 1), (0, -1)]

State = tuple[tuple[int, int], int]


@timing
def main(inp: str) -> None:
    falling_bytes = [
        cast(tuple[int, int], tuple(map(int, row.split(","))))
        for row in inp.split("\n")
    ]
    fallen_bytes = falling_bytes[:FALLEN_MEMORY]
    grid = [["."] * SIZE_X * 2 for _ in range(SIZE_Y)]
    for x, y in fallen_bytes:
        grid[y][x] = "#"
    q: deque[State] = deque()
    visited: dict[tuple[int, int], int] = {}
    q.append(((0, 0), 0))
    while len(q) > 0:
        state = q.popleft()
        (y, x), distance = state
        if (y, x) == (SIZE_Y - 1, SIZE_X - 1):
            print(distance)
            break
        if (y, x) in visited and visited[y, x] <= distance:
            continue
        visited[y, x] = distance
        for dy, dx in DIRECTIONS:
            ny = y + dy
            nx = x + dx
            if 0 <= ny < SIZE_Y and 0 <= nx < SIZE_X and grid[ny][nx] != "#":
                q.append(((ny, nx), distance + 1))


if __name__ == "__main__":
    run_with_prep(main)
