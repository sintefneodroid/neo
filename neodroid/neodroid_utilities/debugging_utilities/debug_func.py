#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import namedtuple
from typing import Callable

__author__ = 'cnheider'

from functools import wraps, partial


def debug_print_return_func(func: callable = None, *, prefix: str = '') -> callable:
  if not func:
    new_debug_func = partial(debug_print_return_func, prefix=prefix)
    return new_debug_func

  msg = prefix + func.__qualname__

  @wraps(func)
  def wrapper(*args, **kwargs):
    print(msg)
    return func(*args, **kwargs)

  return wrapper


def debug_class(cls):
  for [method_key, method_value] in vars(cls).items():
    if isinstance(method_value,Callable):
      setattr(cls, method_key, debug_print_return_func(method_value))
  return cls


class MetaDebugBase(type):
  def __new__(cls, *args, **kwargs):
    class_obj = super().__new__(cls, *args, **kwargs)
    class_obj = debug_class(class_obj)
    return class_obj


class DebugBase(metaclass=MetaDebugBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


if __name__ == '__main__':
  a = 5

  b = namedtuple('Test', ('first', 'second', 'third', 'fourth'))

  c = b(1, 2, 3, 4)


  @debug_print_return_func(prefix='**')
  def aa():
    print('aa')


  @debug_print_return_func
  def bb():
    print('bb')


  class d(DebugBase):

    @staticmethod  # Note no the debug func attribute is no applied to this static method
    def add(a, b):
      return a + b

    def sub(self, a, b):
      return a - b

    def apply(self, a, b, op):
      return op(a, b)


  aa()

  bb()

  print(a)

  print(c.second)

  e = d()

  print(e.apply(a, c.second, e.sub))

  print(e.apply(a, c.second, e.add))
