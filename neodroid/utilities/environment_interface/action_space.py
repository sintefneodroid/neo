#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

from neodroid.models.range import Range
from neodroid.models.space import Space

__author__ = 'cnheider'

import numpy as np


class ActionSpace(Space):

  def parse_action_space(self, action_spaces):
    self._ranges = action_spaces

  def sample(self):
    actions = []
    for valid_input in self._ranges:
      sample = np.random.uniform(valid_input.min_value, valid_input.max_value, 1)
      actions.append(np.round(sample, valid_input.decimal_granularity))
    return [actions]

  def validate(self, actions):
    for i in range(len(actions)):
      clipped = np.clip(actions[i],
                        self._ranges[i].min_value,
                        self._ranges[i].max_value,
                        )
      actions[i] = np.round(clipped, self._ranges[i].decimal_granularity)
    return actions

  @property
  def num_discrete_actions(self):
    return sum([r.discrete_steps for r in self._ranges])

  @property
  def is_singular(self):
    return False  # TODO: Implement

  @property
  def is_discrete(self):
    return np.array([a.decimal_granularity==0 for a in self._ranges]).all()

  @property
  def is_continuous(self):
    return True  # TODO: Implement

  @property
  def is_mixed(self):
    return True  # TODO: Implement

  def discrete_ternary_one_hot_sample(self):
    idx = np.random.randint(0, self.num_motors)
    zeros = np.zeros(self.num_ternary_actions)
    if len(self._ranges) > 0:
      sample = np.random.uniform(
          self._ranges[idx].min_value, self._ranges[idx].max_value, 1
          )
      if sample > 0:
        zeros[idx] = 1
      else:
        zeros[idx + self.num_motors] = 1
    return zeros

  def discrete_binary_one_hot_sample(self):
    idx = np.random.randint(0, self.num_motors)
    zeros = np.zeros(self.num_binary_actions)
    if len(self._ranges) > 0:
      sample = np.random.uniform(
          self._ranges[idx].min_value,
          self._ranges[idx].max_value,
          1
          )
      if sample > 0:
        zeros[idx] = 1
      else:
        zeros[idx + self.num_motors] = 1
    return zeros

  def signed_one_hot_sample(self):
    num = self.num_binary_actions
    return random.randrange(num)

  def discrete_one_hot_sample(self):
    idx = np.random.randint(0, self.num_motors)
    zeros = np.zeros(self.num_motors)
    if len(self._ranges) > 0:
      val = np.random.random_integers(
          self._ranges[idx].min_value(),
          self._ranges[idx].max_value(),
          1,
          )
      zeros[idx] = val
    return zeros

  def discrete_sample(self):
    idx = np.random.randint(0, self.num_binary_actions)
    return idx

  def one_hot_sample(self):

    idx = np.random.randint(0, self.num_motors)
    zeros = np.zeros(self.num_motors)
    if len(self._ranges) > 0:
      zeros[idx] = 1
    return zeros

if __name__ == '__main__':
  acs = ActionSpace([Range(min_value=0,max_value=3,decimal_granularity=2),Range(min_value=0,max_value=2,
                                                                                decimal_granularity=1)])
  print(acs,acs.low,acs.high, acs.decimal_granularity, acs.num_discrete_actions)
