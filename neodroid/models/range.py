#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math

__author__ = 'cnheider'


class Range(object):
  '''

  '''

  def __init__(self,
               decimal_granularity=0,
               min_value=0,
               max_value=0):
    self._decimal_granularity = decimal_granularity
    self._min_value = min_value
    self._max_value = max_value

  @property
  def decimal_granularity(self):
    return self._decimal_granularity

  @property
  def min_value(self):
    return self._min_value

  @property
  def min(self):
    return self.min_value

  @property
  def max_value(self):
    return self._max_value

  @property
  def max(self):
    return self.max_value

  @property
  def discrete_step_size(self):
    return 1 / (1 + self.decimal_granularity)

  @property
  def span(self):
    return self.max_value - self.min_value

  @property
  def discrete_steps(self):
    return math.floor(self.span / self.discrete_step_size) + 1

  def to_dict(self)->dict:
    '''
    >>> type(self.to_dict())
    type(dict)
    :return:
    '''
    return {
      'decimal_granularity':self._decimal_granularity,
      'min_value':          self._min_value,
      'max_value':          self._max_value,
      }

  def __repr__(self):
    return (f'<Range>\n'
            f'<decimal_granularity>{self._decimal_granularity}</decimal_granularity>\n'
            f'<min_value>{self._min_value}</min_value>\n'
            f'<max_value>{self._max_value}</max_value>\n'
            f'</Range>\n')

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()


if __name__ == '__main__':
  acs = Range()
  print(acs)
