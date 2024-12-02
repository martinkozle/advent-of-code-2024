import sys


def eprint(*values: object) -> None:
    print(*values, file=sys.stderr)
