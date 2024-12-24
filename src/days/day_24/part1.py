import re
from typing import Literal

from src.prep import run_with_prep
from src.timing import timing

type Operation = Literal["OR", "AND", "XOR"]
type Wire = str
type Gate = tuple[Wire, Operation, Wire]


def operate(wire1_value: bool, wire2_value: bool, op: Operation) -> bool:
    match op:
        case "OR":
            return wire1_value or wire2_value
        case "AND":
            return wire1_value and wire2_value
        case "XOR":
            return wire1_value ^ wire2_value


class Solver:
    def __init__(
        self,
        gates: dict[Wire, Gate],
        start_values: dict[Wire, bool],
    ) -> None:
        self.values = start_values.copy()
        self.gates = gates

    def rec(self, wire: Wire) -> bool:
        if wire in self.values:
            return self.values[wire]
        gate = self.gates[wire]
        wire1_value = self.rec(gate[0])
        wire2_value = self.rec(gate[2])
        output = operate(wire1_value, wire2_value, gate[1])
        self.values[wire] = output
        return output


@timing
def main(inp: str) -> None:
    start_values_str, gates_str = inp.split("\n\n")
    start_values = {
        row[0:3]: row[5] == "1" for row in start_values_str.strip().split("\n")
    }
    gates: dict[Wire, Gate] = {
        w3: (w1, op, w2)
        for w1, op, w2, w3 in re.findall(
            r"(.+) (\w+) (.+) -> (.+)",
            gates_str,
        )
    }
    z_wires = sorted(
        (wire for wire in gates if wire[0] == "z"),
        key=lambda wire: int(wire[1:]),
        reverse=True,
    )
    solver = Solver(gates, start_values)
    values = [solver.rec(z_wire) for z_wire in z_wires]
    if not all(value is not None for value in values):
        raise RuntimeError("Unexpected state")
    output = int("".join("1" if value else "0" for value in values), 2)
    print(output)


if __name__ == "__main__":
    run_with_prep(main)
