from src.prep import run_with_prep
from src.timing import timing


@timing
def main(inp: str) -> None:
    lines = inp.split("\n")
    search_kernels = [
        [["M", ".", "S"], [".", "A", "."], ["M", ".", "S"]],
        [["M", ".", "M"], [".", "A", "."], ["S", ".", "S"]],
        [["S", ".", "S"], [".", "A", "."], ["M", ".", "M"]],
        [["S", ".", "M"], [".", "A", "."], ["S", ".", "M"]],
    ]
    count = 0
    for start_y in range(len(lines) - 2):
        for start_x in range(len(lines[0]) - 2):
            for search_kernel in search_kernels:
                flag = True
                for dy in range(len(search_kernel)):
                    for dx in range(len(search_kernel[dy])):
                        char = lines[start_y + dy][start_x + dx]
                        target = search_kernel[dy][dx]
                        if target == ".":
                            continue
                        if target != char:
                            flag = False
                            break
                    if not flag:
                        break
                if flag:
                    count += 1
    print(count)


if __name__ == "__main__":
    run_with_prep(main)
