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
    machines_str = inp.split("\n\n")
    machines: list[Machine] = []
    for machine_str in machines_str:
        button_a_str, button_b_str, prize_str = machine_str.split("\n")
        ax, ay = [
            int(coord_str.split("+")[1])
            for coord_str in button_a_str.split(":")[1].split(", ")
        ]
        bx, by = [
            int(coord_str.split("+")[1])
            for coord_str in button_b_str.split(":")[1].split(", ")
        ]
        px, py = [
            int(coord_str.split("=")[1])
            for coord_str in prize_str.split(":")[1].split(", ")
        ]
        machines.append(Machine(ax=ax, ay=ay, bx=bx, by=by, px=px, py=py))

    print(sum(solve(machine) for machine in machines))


if __name__ == "__main__":
    run_with_prep(main)
