#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

import collections
import threading
from contextlib import contextmanager

_tls = threading.local()


@contextmanager
def _nested():
  _tls.level = getattr(_tls, 'level', 0) + 1
  try:
    yield '   ' * _tls.level
  finally:
    _tls.level -= 1


@contextmanager
def _recursion_lock(obj):
  if not hasattr(_tls, 'history'):
    _tls.history = []  # can't use set(), not all objects are hashable
  if obj in _tls.history:
    yield True
    return
  _tls.history.append(obj)
  try:
    yield False
  finally:
    _tls.history.pop(-1)


def pretty_print(cls):
  def __repr__(self):
    if getattr(_tls, 'level', 0) > 0:
      return str(self)
    else:
      attrs = ', '.join('%s = %r' % (k, v) for k, v in self.__dict__.items())
      return '%s(%s)' % (self.__class__.__name__, attrs)

  def __str__(self):
    with _recursion_lock(self) as locked:
      if locked:
        return '<...>'
      with _nested() as indent:
        attrs = []
        for k, v in self.__dict__.items():
          if k.startswith('_'):
            continue
          if isinstance(v, (list, tuple, collections.Sequence)) and v:
            attrs.append(f'{indent}{k} = [')
            with _nested() as indent2:
              for item in v:
                attrs.append(f'{indent2}{item!r},')
            attrs.append(f'{indent}]')
          elif isinstance(v, (dict, collections.Mapping)) and v:
            attrs.append(f'{indent}{k} = (')
            with _nested() as indent2:
              for k2, v2 in v.items():
                attrs.append(f'{indent2}{k2!r}: {v2!r},')
            attrs.append(f'{indent})')
          else:
            attrs.append(f'{indent}{k} = {v!r}')
        if not attrs:
          return f'{self.__class__.__name__}()'
        else:
          attrsss = '\n'.join(attrs)
          return f"{self.__class__.__name__}:\n{attrsss}"

  cls.__repr__ = __repr__
  cls.__str__ = __str__
  return cls
