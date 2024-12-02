def parse_line_ints(inp: str) -> list[list[int]]:
    return [list(map(int, line.split())) for line in inp.split("\n")]
