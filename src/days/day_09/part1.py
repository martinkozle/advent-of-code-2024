from src.prep import run_with_prep
from src.timing import timing


@timing
def main(inp: str) -> None:
    disk: list[int] = []
    for i in range(0, len(inp), 2):
        block_id = i // 2
        disk += [block_id] * int(inp[i])
        if i + 1 < len(inp):
            disk += [-1] * int(inp[i + 1])

    change = True
    while change:
        change = False
        l_ind = 0
        r_ind = len(disk) - 1
        while l_ind < r_ind:
            while disk[l_ind] != -1:
                l_ind += 1

            while disk[r_ind] == -1:
                r_ind -= 1

            if l_ind >= r_ind:
                break

            disk[l_ind] = disk[r_ind]
            disk[r_ind] = -1
            change = True

    checksum = 0
    for i, v in enumerate(disk):
        if v == -1:
            continue
        checksum += v * i

    print(checksum)


if __name__ == "__main__":
    run_with_prep(main)
