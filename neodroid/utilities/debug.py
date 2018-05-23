#!/usr/bin/env python3
# coding=utf-8
import typing
from collections import namedtuple
from typing import Callable

__author__ = 'cnheider'

import warnings
from enum import Enum
from functools import wraps, partial


def debug_func(func: Callable = None, *, prefix: str = '') -> Callable:
  if not func:
    new_debug_func = partial(debug_func, prefix=prefix)
    return new_debug_func

  msg = prefix + func.__qualname__

  @wraps(func)
  def wrapper(*args, **kwargs):
    print(msg)
    return func(*args, **kwargs)

  return wrapper


def debug_class(cls):
  for method_key, method_value in vars(cls).items():
    if callable(method_value):
      setattr(cls, method_key, debug_func(method_value))

  return cls


class DebugBase(type):
  def __new__(cls, *args, **kwargs):
    class_obj = super().__new__(cls, *args, **kwargs)
    class_obj = debug_class(class_obj)
    return class_obj


class Base(metaclass=DebugBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


class ClientEvents(Enum):
  CONNECTED = 1  # auto()
  DISCONNECTED = 2  # auto()
  TIMEOUT = 3  # auto()


def debug_print(msg='empty debug message'):
  print(msg)


def print_return(f):
  @wraps(f)
  def call_f(*args, **kwargs):
    call_return = f(*args, **kwargs)
    if 'verbose' in kwargs and kwargs['verbose']:
      print(call_return)
    return call_return

  return call_f


def message_client_event(event):
  def receive_f(f):

    @wraps(f)
    def call_f(ctx, *args, **kwargs):
      if event is ClientEvents.CONNECTED:
        warnings.warn('Connected to server')
      elif event is ClientEvents.DISCONNECTED:
        warnings.warn('Disconnected from server')
      elif event is ClientEvents.TIMEOUT:
        warnings.warn('Connection timeout')
      return f(ctx, *args, **kwargs)

    return call_f

  return receive_f


if __name__ == '__main__':
  a = 5

  b = namedtuple('Test', ('first', 'second', 'third', 'fourth'))

  c = b(1, 2, 3, 4)


  @debug_func(prefix='**')
  def aa():
    print('aa')


  @debug_func
  def bb():
    print('bb')


  class d(Base):

    @staticmethod #Note no the debug func attribute is no applied to this static method
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
