#!/usr/bin/env python3
# coding=utf-8
import math

__author__ = 'cnheider'


class Space(object):

  def __init__(self, decimal_granularity, min_value, max_value):
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
  def max_value(self):
    return self._max_value
  @property
  def discrete_step_size(self):
    return 1 / (1 + self.decimal_granularity)
  @property
  def span(self):
    return self.max_value -self.min_value
  @property
  def discrete_steps(self):
    return math.floor(self.span / self.discrete_step_size)+1

  def to_dict(self):
    return {
      'decimal_granularity':  self._decimal_granularity,
      'min_value': self._min_value,
      'max_value':self._max_value,
      }

  def __repr__(self):
    return '<InputRange>\n' + '  <decimal_granularity>' + str(
        self._decimal_granularity
        ) + '</decimal_granularity>\n' + '  <min_value>' + str(
        self._min_value
        ) + '</min_value>\n' + '  <max_value>' + str(
        self._max_value
        ) + '</max_value>\n' + '</InputRange>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
