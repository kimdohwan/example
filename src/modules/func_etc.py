import io
import os
import time
import zipfile
from abc import *
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

    @staticmethod
    def save_zip(content: bytes, dir_path: str, filename: str):
        z = zipfile.ZipFile(io.BytesIO(content))
        z.extractall(os.path.join(dir_path, filename))


class ReqBaseException(Exception):
    pass


class ReqBase(metaclass=ABCMeta):
    method: str = None
    url: str = None

    def __init__(self):
        self._res = None

    @abstractmethod
    def is_valid(self, res):
        pass

    @property
    def req_kwargs(self):
        raise ReqBaseException('req_kwargs() is not defined')

    def set_res(self, res):
        self._res = res


