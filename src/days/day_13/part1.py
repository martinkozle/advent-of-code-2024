import re
from dataclasses import dataclass

from src.prep import run_with_prep
from src.timing import timing


@dataclass
class Machine:
    ax: int
    ay: int
    bx: int
    by: int
    px: int
    py: int


def solve(machine: Machine) -> int:
    minim: int | None = None
    for a in range(100):
        for b in range(100):
            if (
                a * machine.ax + b * machine.bx == machine.px
                and a * machine.ay + b * machine.by == machine.py
                and a * 3 + b < (minim or 10**63)
            ):
                minim = a * 3 + b
    return minim or 0


@timing
def main(inp: str) -> None:
    matches = re.findall(
        r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\n"
        r"Prize: X=(\d+), Y=(\d+)",
        inp,
    )
    machines = [
        Machine(ax=ax, ay=ay, bx=bx, by=by, px=px, py=py)
        for ax, ay, bx, by, px, py in (map(int, match) for match in matches)
    ]

    print(sum(solve(machine) for machine in machines))


if __name__ == "__main__":
    run_with_prep(main)
