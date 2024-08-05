from functools import wraps

from src.helpers import metric


def timeit(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        with metric.timer("TIMEIT {}".format(f.__name__)):
            return f(*args, **kwargs)
    return decorated
