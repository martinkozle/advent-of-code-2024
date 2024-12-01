import sys

from src.timing import timing


@timing
def main(inp: str) -> None:
    pass


if __name__ == "__main__":
    sys.setrecursionlimit(2**31 - 1)
    sys.set_int_max_str_digits(2**31 - 1)
    main(sys.stdin.read())
