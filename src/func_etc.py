import time
from contextlib import contextmanager


class Func:
    @staticmethod
    @contextmanager
    def check_time():
        s = time.time()
        yield None
        e = time.time()
        print(f'{e - s} sec')

    @staticmethod
    def print_func_name(func):
        def a(*args, **kwargs):
            print(func.__name__)
            return func(*args, **kwargs)

        return a
