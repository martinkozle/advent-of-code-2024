from collections import deque
from collections.abc import Iterable
from itertools import groupby

from src.prep import run_with_prep
from src.timing import timing

DIRECTIONS: list[tuple[int, int]] = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def flood(grid: list[str], loc: tuple[int, int]) -> set[tuple[int, int]]:
    size_y = len(grid)
    size_x = len(grid[0])
    visited: set[tuple[int, int]] = set()
    q: deque[tuple[int, int]] = deque()
    q.append(loc)
    while len(q):
        loc = q.popleft()
        if loc in visited:
            continue
        y, x = loc
        if not (0 <= y < size_y and 0 <= x < size_x):
            continue
        visited.add(loc)
        for dy, dx in DIRECTIONS:
            ny = y + dy
            nx = x + dx
            if not (0 <= ny < size_y and 0 <= nx < size_x):
                continue
            if grid[y][x] == grid[ny][nx]:
                q.append((ny, nx))
    return visited


def calculate_sides(grid: list[str], region: Iterable[tuple[int, int]]) -> int:
    size_y = len(grid)
    size_x = len(grid[0])
    borders: list[tuple[tuple[int, int], tuple[int, int]]] = []
    for y, x in region:
        for dy, dx in DIRECTIONS:
            ny = y + dy
            nx = x + dx
            if (0 <= ny < size_y and 0 <= nx < size_x) and grid[y][x] == grid[ny][nx]:
                continue
            borders.append(((y, x), (dy, dx)))

    sides = 0
    for (dx, _), same_facing_borders in groupby(
        sorted(borders, key=lambda x: x[1]),
        key=lambda x: x[1],
    ):
        locations = [(y, x) for (y, x), _ in same_facing_borders]
        if dx != 0:
            for _, same_y_borders in groupby(
                sorted(locations, key=lambda x: x[0]),
                key=lambda x: x[0],
            ):
                sides += num_increasing_ranges([x for (_, x) in same_y_borders])
        else:
            for _, same_x_borders in groupby(
                sorted(locations, key=lambda x: x[1]),
                key=lambda x: x[1],
            ):
                sides += num_increasing_ranges([y for (y, _) in same_x_borders])

    return sides


def num_increasing_ranges(iterable: Iterable[int]) -> int:
    num = 0
    prev_x = -10
    for x in sorted(iterable):
        if x != prev_x + 1:
            num += 1
        prev_x = x
    return num


@timing
def main(inp: str) -> None:
    grid = inp.split("\n")
    visited: set[tuple[int, int]] = set()
    size_y = len(grid)
    size_x = len(grid[0])
    price = 0
    for y in range(size_y):
        for x in range(size_x):
            if (y, x) in visited:
                continue
            region = flood(grid=grid, loc=(y, x))
            visited |= region
            sides = calculate_sides(grid, region)
            area = len(region)
            price += sides * area
    print(price)


if __name__ == "__main__":
    run_with_prep(main)
