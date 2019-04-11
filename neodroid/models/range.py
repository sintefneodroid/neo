#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math

import numpy as np

__author__ = 'cnheider'


class Range(object):
  '''

  '''

  def __init__(self,
               *,
               min_value=0,
               max_value=0,
               decimal_granularity=0):
    assert max_value >= min_value
    assert decimal_granularity >= 0

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
    return 1 / np.power(10,self.decimal_granularity)

  @property
  def span(self):
    return self.max_value - self.min_value

  @property
  def discrete_steps(self):
    return math.floor(self.span / self.discrete_step_size)+1

  def to_dict(self) -> dict:
    '''

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

  def sample(self):
    if self.decimal_granularity == 0:
      return self.cheapest_sample()

    return self.cheaper_sample()
    #return self.expensive_sample()

  def cheapest_sample(self):
    return np.random.randint(self.min, self.max+1)

  def cheaper_sample(self):
    return np.round(np.random.random() * self.span,self.decimal_granularity)

  def expensive_sample(self):
    return np.random.choice(np.linspace(self.min, self.max, num=self.discrete_steps))


if __name__ == '__main__':
  r = Range(min_value=0,max_value=5,decimal_granularity=2)
  print(r,r.sample())
