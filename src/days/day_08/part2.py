from src.prep import run_with_prep
from src.timing import timing


@timing
def main(inp: str) -> None:
    nodes_dict: dict[str, list[tuple[int, int]]] = {}
    lines = inp.split("\n")
    size_y = len(lines)
    size_x = len(lines[0])
    for y in range(size_y):
        for x in range(size_x):
            n = lines[y][x]
            if n != ".":
                nodes_dict.setdefault(n, []).append((y, x))

    antinode_coords: set[tuple[int, int]] = set()
    for coords in nodes_dict.values():
        for y1, x1 in coords:
            for y2, x2 in coords:
                if (y1, x1) == (y2, x2):
                    continue
                for i in range(1_000_000):
                    ay, ax = (y2 + (y2 - y1) * i, x2 + (x2 - x1) * i)
                    if not (0 <= ay < size_y and 0 <= ax < size_x):
                        break
                    antinode_coords.add((ay, ax))

    print(len(antinode_coords))


if __name__ == "__main__":
    run_with_prep(main)
