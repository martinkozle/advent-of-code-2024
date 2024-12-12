from collections import deque
from collections.abc import Iterable

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


def calculate_perimeter(grid: list[str], region: Iterable[tuple[int, int]]) -> int:
    size_y = len(grid)
    size_x = len(grid[0])
    perimeter = 0
    for y, x in region:
        for dy, dx in DIRECTIONS:
            ny = y + dy
            nx = x + dx
            if not (0 <= ny < size_y and 0 <= nx < size_x):
                perimeter += 1
                continue

            if grid[y][x] != grid[ny][nx]:
                perimeter += 1
    return perimeter


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
            perimeter = calculate_perimeter(grid, region)
            area = len(region)
            price += perimeter * area
    print(price)


if __name__ == "__main__":
    run_with_prep(main)
