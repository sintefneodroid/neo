#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Iterable

from .range import Range

__author__ = 'cnheider'


class Space(object):

  def __init__(self, ranges: Iterable[Range] = (), discrete_binary=False):
    if not isinstance(ranges, Iterable):
      ranges = [ranges]
    self._ranges = ranges
    self._discrete_binary = discrete_binary

  @property
  @abstractmethod
  def ranges(self) -> Iterable[Range]:
    return self._ranges

  def sample(self) -> Iterable[float]:
    return [r.sample() for r in self._ranges]

  @property
  def low(self):
    return [motion_space.min_value for motion_space in self._ranges]

  @property
  def high(self):
    return [motion_space.max_value for motion_space in self._ranges]

  @property
  def max(self):
    return self.high

  @property
  def min(self):
    return self.low

  @property
  def decimal_granularity(self):
    return [motion_space.decimal_granularity for motion_space in self._ranges]

  @property
  def shape(self):
    if self._discrete_binary:
      return self.discrete_binary_shape

    return self.continuous_shape

  @property
  def discrete_binary_shape(self):
    return len(self._ranges) * 2, 1

  @property
  def continuous_shape(self):
    return len(self._ranges), 1

  def __repr__(self):
    ranges_str = ''.join([str(range.__repr__()) for range in self._ranges])

    return (f'<Space>\n'
            f'<Ranges>\n{ranges_str}</Ranges>\n'
            f'</Space>\n')

  @property
  def n(self):
    return len(self)

  def __len__(self):
    return len(self._ranges)


if __name__ == '__main__':
  acs = Space()
  print(acs, acs.decimal_granularity)
