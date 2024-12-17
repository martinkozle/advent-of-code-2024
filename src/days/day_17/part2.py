import re

from src.prep import run_with_prep
from src.timing import timing


def execute_program(registers: dict[str, int], program: list[int]) -> list[int]:
    pointer = 0
    outputs: list[int] = []
    while True:
        if pointer >= len(program):
            break
        opcode = program[pointer]
        operand = program[pointer + 1]
        operand_value: int
        match operand:
            case 0 | 1 | 2 | 3:
                operand_value = operand
            case 4:
                operand_value = registers["A"]
            case 5:
                operand_value = registers["B"]
            case 6:
                operand_value = registers["C"]
            case _:
                operand_value = operand
        match opcode:
            case 0:
                registers["A"] = registers["A"] // 2**operand_value
            case 1:
                registers["B"] = registers["B"] ^ operand
            case 2:
                registers["B"] = operand_value % 8
            case 3:
                if registers["A"] != 0:
                    pointer = operand
                    continue
            case 4:
                registers["B"] = registers["B"] ^ registers["C"]
            case 5:
                outputs.append(operand_value % 8)
            case 6:
                registers["B"] = registers["A"] // 2**operand_value
            case 7:
                registers["C"] = registers["A"] // 2**operand_value
        pointer += 2
    return outputs


@timing
def main(inp: str) -> None:
    registers: dict[str, int] = {}
    for register in ("A", "B", "C"):
        match = re.search(rf"Register {register}: (-?\d+)", inp)
        if match is None:
            raise RuntimeError("Unexpected state")
        registers[register] = int(match.group(1))
    match = re.search(r"Program: ((\d+,)+\d+)", inp)
    if match is None:
        raise RuntimeError("Unexpected state")
    program = list(map(int, match.group(1).split(",")))
    exec_program = program[:-2]
    a = 0
    for ind in range(len(program)):
        # shift by 3 bits
        a *= 8
        for a_mod in range(16):
            out, *_ = execute_program(registers | {"A": a + a_mod}, exec_program)
            if program[len(program) - 1 - ind] == out:
                a = a + a_mod
                break
        else:
            raise RuntimeError("Unexpected state")
    print(a)


if __name__ == "__main__":
    run_with_prep(main)
