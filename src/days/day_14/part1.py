import re
from collections.abc import Iterable
from dataclasses import dataclass

from src.prep import run_with_prep
from src.timing import timing

SECONDS = 100
TILES_WIDE = 101
TILES_TALL = 103


@dataclass
class Robot:
    px: int
    py: int
    vx: int
    vy: int


def matrix_repr(robots: Iterable[Robot]) -> str:
    matrix = [["."] * TILES_WIDE for _ in range(TILES_TALL)]
    for robot in robots:
        if matrix[robot.py][robot.px] == ".":
            matrix[robot.py][robot.px] = "0"
        matrix[robot.py][robot.px] = str(int(matrix[robot.py][robot.px]) + 1)

    return "\n".join("".join(row) for row in matrix)


@timing
def main(inp: str) -> None:
    matches = re.findall(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", inp)
    robots = [
        Robot(px=px, py=py, vx=vx, vy=vy)
        for px, py, vx, vy in (map(int, match) for match in matches)
    ]

    quadrants: list[int] = [0, 0, 0, 0]
    for robot in robots:
        robot.px = (robot.px + robot.vx * SECONDS) % TILES_WIDE
        robot.py = (robot.py + robot.vy * SECONDS) % TILES_TALL
        if robot.px < TILES_WIDE // 2:
            if robot.py < TILES_TALL // 2:
                quadrants[0] += 1
            elif robot.py > TILES_TALL // 2:
                quadrants[1] += 1
        elif robot.px > TILES_WIDE // 2:
            if robot.py < TILES_TALL // 2:
                quadrants[2] += 1
            elif robot.py > TILES_TALL // 2:
                quadrants[3] += 1
    # eprint(matrix_repr(robots))
    # eprint(quadrants)
    print(quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3])


if __name__ == "__main__":
    run_with_prep(main)
