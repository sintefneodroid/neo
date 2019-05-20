#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

import neodroid.messaging


class Sensor(object):
  '''

  '''

  def __init__(self, sensor_name, observation_space, observation_value):
    self._observation_space = observation_space
    self._sensor_name = sensor_name
    self._observation_value = observation_value

  @property
  def name(self):
    return self._sensor_name

  @property
  def space(self):
    if self._observation_space:
      space = neodroid.messaging.deserialise_space(self._observation_space)
      return space

  @property
  def value(self):
    return self._observation_value

  def __repr__(self):
    return (f'<Observer>\n'
            f'<observation_name>{self._sensor_name}</observation_name>\n'
            f'<observation_space>{self.space}</observation_space>\n'
            f'<observation_value>{self.value}</observation_value>\n'
            f'</Observer>\n')

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()

  def __float__(self):
    return float(self.value)

  def __int__(self):
    return int(self.value)

  def __call__(self, *args, **kwargs):
    return self.value

  def __cmp__(self, other):
    return self.value == other

  def __next__(self):
    return self.value
