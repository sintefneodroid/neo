#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from neodroid.interfaces.environment_models import Range, Space

__author__ = 'cnheider'

import numpy as np


class SignalSpace(Space):

  def parse_action_space(self, action_spaces):
    self._ranges = action_spaces

  def sample(self):
    actions = []
    for valid_input in self._ranges:
      sample = np.random.uniform(valid_input.min_value, valid_input.max_value, 1)
      actions.append(np.round(sample, valid_input.decimal_granularity))
    return actions

  def validate(self, actions):
    for i in range(len(actions)):
      clipped = np.clip(actions[i],
                        self._ranges[i].min_value,
                        self._ranges[i].max_value,
                        )
      actions[i] = np.round(clipped, self._ranges[i].decimal_granularity)
    return actions

  @property
  def solved_threshold(self):
    return False  # TODO: Implement

  @property
  def is_sparse(self):
    return np.array([a.decimal_granularity == 0 for a in self._ranges]).all()


if __name__ == '__main__':
  acs = SignalSpace([Range(min_value=0, max_value=3, decimal_granularity=2),
                     Range(min_value=0, max_value=2, decimal_granularity=1)])
  print(acs, acs.low, acs.high, acs.decimal_granularity)
