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
    det = machine.ax * machine.by - machine.ay * machine.bx
    if det == 0:
        return 0
    a1 = machine.px * machine.by - machine.py * machine.bx
    if a1 % det != 0:
        return 0
    a = a1 // det
    b1 = machine.ax * machine.py - machine.ay * machine.px
    if b1 % det != 0:
        return 0
    b = b1 // det
    return a * 3 + b


@timing
def main(inp: str) -> None:
    matches = re.findall(
        r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\n"
        r"Prize: X=(\d+), Y=(\d+)",
        inp,
    )
    machines = [
        Machine(
            ax=ax,
            ay=ay,
            bx=bx,
            by=by,
            px=10000000000000 + px,
            py=10000000000000 + py,
        )
        for ax, ay, bx, by, px, py in (map(int, match) for match in matches)
    ]

    print(sum(solve(machine) for machine in machines))


if __name__ == "__main__":
    run_with_prep(main)
