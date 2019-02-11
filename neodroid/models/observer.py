#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

import neodroid.messaging


class Observer(object):
  '''

  '''

  def __init__(self, observation_name, observation_space, observation_value):
    self._observation_space = observation_space
    self._observation_name = observation_name
    self._observation_value = observation_value

  @property
  def observer_name(self):
    return self._observation_name

  @property
  def observation_space(self):
    if self._observation_space:
      space = neodroid.messaging.deserialise_space(self._observation_space)
      return space

  @property
  def observation_value(self):
    return self._observation_value

  def __repr__(self):
    return (f'<Observer>\n'
            f'<observation_name>{self._observation_name}</observation_name>\n'
            f'<observation_space>{self.observation_space}</observation_space>\n'
            f'<observation_value>{self.observation_value}</observation_value>\n'
            f'</Observer>\n')

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()

  def __float__(self):
    return float(self.observation_value)

  def __int__(self):
    return int(self.observation_value)

  def __call__(self, *args, **kwargs):
    return self.observation_value

  def __cmp__(self, other):
    return self.observation_value == other

  def __next__(self):
    return self.observation_value
