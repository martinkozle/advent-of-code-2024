import time
from collections.abc import Callable
from functools import wraps

from src.printing import eprint


def timing[**P, O](f: Callable[P, O]) -> Callable[P, O]:
    @wraps(f)
    def wrap(*args: P.args, **kwargs: P.kwargs) -> O:
        time_start = time.time()
        result = f(*args, **kwargs)
        time_end = time.time()
        eprint(f"Function: `{f.__name__}` took: {time_end - time_start:2.4f} seconds")
        return result

    return wrap
