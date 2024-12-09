from src.prep import run_with_prep
from src.timing import timing


@timing
def main(inp: str) -> None:
    disk: list[int] = []
    sizes: dict[int, int] = {}
    block_locations: dict[int, int] = {}
    blocks: list[int] = []
    for i in range(0, len(inp), 2):
        block_id = i // 2
        block_locations[block_id] = len(disk)
        blocks.append(block_id)
        disk += [block_id] * int(inp[i])
        sizes[block_id] = int(inp[i])
        if i + 1 < len(inp):
            disk += [-1] * int(inp[i + 1])

    while True:
        found_space = False
        l_ind = 0
        block_ind = len(blocks) - 1
        while True:
            while blocks[block_ind] == -1:
                block_ind -= 1
                if block_ind < 0:
                    break

            if block_ind < 0:
                break

            while l_ind < len(disk):
                while disk[l_ind] != -1:
                    l_ind += 1
                    if l_ind >= len(disk):
                        break

                if l_ind >= len(disk):
                    break

                if l_ind >= block_locations[blocks[block_ind]]:
                    break
                free_space = 0
                while l_ind + free_space < len(disk) and disk[l_ind + free_space] == -1:
                    free_space += 1

                if sizes[blocks[block_ind]] > free_space:
                    l_ind += free_space
                    continue

                found_space = True
                break

            if found_space:
                break

            block_ind -= 1
            l_ind = 0

        if not found_space:
            break

        r_ind = block_locations[blocks[block_ind]]
        block_id = disk[r_ind]
        while r_ind < len(disk) and disk[r_ind] == block_id:
            disk[l_ind] = disk[r_ind]
            disk[r_ind] = -2
            l_ind += 1
            r_ind += 1

        blocks[block_ind] = -1
        # eprint("".join("." if v < 0 else str(v) for v in disk))

    checksum = 0
    for i, v in enumerate(disk):
        if v < 0:
            continue
        checksum += v * i

    print(checksum)


if __name__ == "__main__":
    run_with_prep(main)
