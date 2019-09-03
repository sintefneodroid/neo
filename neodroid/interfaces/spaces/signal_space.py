#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from neodroid.interfaces.spaces import Space, EnvironmentDescription, Sequence
from neodroid.interfaces.spaces.range import Range

__author__ = 'Christian Heider Nielsen'

import numpy


class SignalSpace(Space):

  def parse_action_space(self, action_spaces):
    self._ranges = action_spaces

  def sample(self):
    actions = []
    for valid_input in self._ranges:
      sample = numpy.random.uniform(valid_input.min_value, valid_input.max_value, 1)
      actions.append(numpy.round(sample, valid_input.decimal_granularity))
    return actions

  def validate(self, actions):
    for i in range(len(actions)):
      clipped = numpy.clip(actions[i],
                           self._ranges[i].min_value,
                           self._ranges[i].max_value,
                           )
      actions[i] = numpy.round(clipped, self._ranges[i].decimal_granularity)
    return actions

  @property
  def solved_threshold(self):
    return False  # TODO: Implement

  @property
  def is_sparse(self):
    return numpy.array([a.decimal_granularity == 0 for a in self._ranges]).all()

  @staticmethod
  def from_environment_description(environment_description: EnvironmentDescription):
    return None
    '''
    sensor_names = environment_description.signal_space
    observation_spaces = []
    observers = environment_description.sensors.values()
    for observer in observers:
      if isinstance(observer.space, Sequence):
        for r in observer.space:
          observation_spaces.append(r)
      else:
        observation_spaces.append(observer.space)

    return SignalSpace(observation_spaces, sensor_names)
    '''

if __name__ == '__main__':
  acs = SignalSpace([Range(min_value=0, max_value=3, decimal_granularity=2),
                     Range(min_value=0, max_value=2, decimal_granularity=1)], ())
  print(acs, acs.low, acs.high, acs.decimal_granularity)
