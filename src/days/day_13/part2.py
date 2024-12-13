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
        machines.append(
            Machine(
                ax=ax,
                ay=ay,
                bx=bx,
                by=by,
                px=px + 10000000000000,
                py=py + 10000000000000,
            ),
        )

    print(sum(solve(machine) for machine in machines))


if __name__ == "__main__":
    run_with_prep(main)
