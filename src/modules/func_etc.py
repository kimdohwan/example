import io
import os
import re
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


class ReqBaseVAlidator(ABC):

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class HttpMethod(ReqBaseVAlidator):
    def __init__(self, *methods):
        self.methods = set(methods)

    def validate(self, value):
        if value not in self.methods:
            raise ValueError(f'choose in {self.methods}')


class URL(ReqBaseVAlidator):
    def __init__(self):
        pass

    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f'value({value}) is not str()')
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if not bool(re.match(regex, value)):
            raise ValueError(f'{value} is not url form')


class ReqBase:
    method = HttpMethod('get', 'post')
    url = URL()

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

print(1)

# class ReqBase(metaclass=ABCMeta):
#     method: str = None
#     url: str = None
#
#     def __init__(self):
#         self._res = None
#
#     @abstractmethod
#     def is_valid(self, res):
#         pass
#
#     @property
#     def req_kwargs(self):
#         raise ReqBaseException('req_kwargs() is not defined')
#
#     def set_res(self, res):
#         self._res = res


