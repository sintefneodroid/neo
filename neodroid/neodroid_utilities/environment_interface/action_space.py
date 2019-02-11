#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

from neodroid.models.range import Range
from neodroid.models.space import Space

__author__ = 'cnheider'

import numpy as np


class ActionSpace(Space):

  @property
  def ranges(self):
    return self._action_spaces

  def parse_action_space(self, action_spaces):
    self._action_spaces = action_spaces

  def sample(self):
    actions = []
    for valid_input in self._action_spaces:
      sample = np.random.uniform(valid_input.min_value, valid_input.max_value, 1)
      actions.append(np.round(sample, valid_input.decimal_granularity))
    return actions

  def validate(self, actions):
    for i in range(len(actions)):
      clipped = np.clip(actions[i],
                        self._action_spaces[i].min_value,
                        self._action_spaces[i].max_value,
                        )
      actions[i] = np.round(clipped, self._action_spaces[i].decimal_granularity)
    return actions

  @property
  def shape(self):
    return [self.num_motors]

  @property
  def n(self):
    return self.num_motors

  @property
  def low(self):
    return [motion_space.min_value() for motion_space in self._action_spaces]

  @property
  def high(self):
    return [motion_space.max_value() for motion_space in self._action_spaces]

  @property
  def num_motors(self):
    return len(self._action_spaces)

  @property
  def discrete_actions(self):
    a = self._action_spaces[0]
    discrete_actions = np.arange(a.min, a.max + 1, np.power(10, a.decimal_granularity))
    return discrete_actions

  @property
  def num_discrete_actions(self):
    return len(self.discrete_actions)

  @property
  def num_binary_actions(self):
    return len(self._action_spaces) * 2

  @property
  def num_ternary_actions(self):
    return len(self._action_spaces) * 3

  @property
  def is_singular(self):
    return False  # TODO: Implement

  @property
  def is_discrete(self):
    return True  # TODO: Implement

  @property
  def is_continuous(self):
    return True  # TODO: Implement

  @property
  def is_mixed(self):
    return True  # TODO: Implement

  def discrete_ternary_one_hot_sample(self):
    idx = np.random.randint(0, self.num_motors)
    zeros = np.zeros(self.num_ternary_actions)
    if len(self._action_spaces) > 0:
      sample = np.random.uniform(
          self._action_spaces[idx].min_value, self._action_spaces[idx].max_value, 1
          )
      if sample > 0:
        zeros[idx] = 1
      else:
        zeros[idx + self.num_motors] = 1
    return zeros

  def discrete_binary_one_hot_sample(self):
    idx = np.random.randint(0, self.num_motors)
    zeros = np.zeros(self.num_binary_actions)
    if len(self._action_spaces) > 0:
      sample = np.random.uniform(
          self._action_spaces[idx].min_value,
          self._action_spaces[idx].max_value,
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
    if len(self._action_spaces) > 0:
      val = np.random.random_integers(
          self._action_spaces[idx].min_value(),
          self._action_spaces[idx].max_value(),
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
    if len(self._action_spaces) > 0:
      zeros[idx] = 1
    return zeros

  def __call__(self, *args, **kwargs):
    return self.shape

  def __len__(self):
    return len(self.shape)

  # def __int__(self):
  #  return int(sum(self.shape))


if __name__ == '__main__':
  acs =ActionSpace()
  acs.parse_action_space([Range()])
  print(acs)
