import sys
from collections.abc import Callable


def run_with_prep[O](f: Callable[[str], O]) -> O:
    sys.setrecursionlimit(2**31 - 1)
    sys.set_int_max_str_digits(2**31 - 1)
    return f(sys.stdin.read().strip())
