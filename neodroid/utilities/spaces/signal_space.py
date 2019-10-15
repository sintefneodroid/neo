#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math

import numpy

from neodroid.utilities.spaces import Space
from neodroid.utilities.spaces import Range

__author__ = 'Christian Heider Nielsen'


class SignalSpace(Space):

  def parse_signal_space(self,
                         signal_range: Range,
                         solved_threshold=math.inf):
    self._ranges = [signal_range]
    self.solved_threshold = solved_threshold

  def is_solved(self, value) -> bool:
    return value > self.solved_threshold

  @property
  def is_sparse(self) -> bool:
    return numpy.array([a.decimal_granularity == 0 for a in self._ranges]).all()


if __name__ == '__main__':
  acs = SignalSpace([Range(min_value=0, max_value=3, decimal_granularity=2),
                     Range(min_value=0, max_value=2, decimal_granularity=1)], ())
  print(acs, acs.low, acs.high, acs.decimal_granularity)
