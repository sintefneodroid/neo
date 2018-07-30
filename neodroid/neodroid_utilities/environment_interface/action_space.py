#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid import Space

__author__ = 'cnheider'

import numpy as np


class ActionSpace(Space):

  def parse_valid_inputs(self, valid_inputs):
    self._valid_inputs = valid_inputs

  def sample(self):
    actions = []
    for valid_input in self._valid_inputs:
      sample = np.random.uniform(valid_input.min_value, valid_input.max_value, 1)
      actions.append(np.round(sample, valid_input.decimal_granularity))
    return actions

  def validate(self, actions):
    for i in range(len(actions)):
      clipped = np.clip(
          actions[i],
          self._valid_inputs[i].min_value,
          self._valid_inputs[i].max_value,
          )
      actions[i] = np.round(clipped, self._valid_inputs[i].decimal_granularity)
    return actions

  @property
  def shape(self):
    return [self.num_motors]

  @property
  def n(self):
    return self.num_motors

  @property
  def low(self):
    return [motion_space.min_value() for motion_space in self._valid_inputs]

  @property
  def high(self):
    return [motion_space.max_value() for motion_space in self._valid_inputs]

  @property
  def num_motors(self):
    return len(self._valid_inputs)

  @property
  def discrete_actions(self):
    a = self._valid_inputs[0]
    discrete_actions = np.arange(a.min, a.max+1, np.power(10,a.decimal_granularity))
    return discrete_actions

  @property
  def num_discrete_actions(self):
    return len(self.discrete_actions)

  @property
  def num_binary_actions(self):
    return len(self._valid_inputs) * 2

  @property
  def num_ternary_actions(self):
    return len(self._valid_inputs) * 3

  @property
  def is_singular(self):
    return False  # TODO: Implement

  @property
  def is_discrete(self):
    return True  # TODO: Implement

  @property
  def is_continuous(self):
    return True  # TODO: Implement

  def discrete_ternary_one_hot_sample(self):
    idx = np.random.randint(0, self.num_motors)
    zeros = np.zeros(self.num_ternary_actions)
    if len(self._valid_inputs) > 0:
      sample = np.random.uniform(
          self._valid_inputs[idx].min_value, self._valid_inputs[idx].max_value, 1
          )
      if sample > 0:
        zeros[idx] = 1
      else:
        zeros[idx + self.num_motors] = 1
    return zeros

  def discrete_binary_one_hot_sample(self):
    idx = np.random.randint(0, self.num_motors)
    zeros = np.zeros(self.num_binary_actions)
    if len(self._valid_inputs) > 0:
      sample = np.random.uniform(
          self._valid_inputs[idx].min_value, self._valid_inputs[idx].max_value, 1
          )
      if sample > 0:
        zeros[idx] = 1
      else:
        zeros[idx + self.num_motors] = 1
    return zeros

  def discrete_one_hot_sample(self):
    idx = np.random.randint(0, self.num_motors)
    zeros = np.zeros(self.num_motors)
    if len(self._valid_inputs) > 0:
      val = np.random.random_integers(
          self._valid_inputs[idx].min_value(),
          self._valid_inputs[idx].max_value(),
          1,
          )
      zeros[idx] = val
    return zeros

  def one_hot_sample(self):

    idx = np.random.randint(0, self.num_motors)
    zeros = np.zeros(self.num_motors)
    if len(self._valid_inputs) > 0:
      zeros[idx] = 1
    return zeros

  def __call__(self, *args, **kwargs):
    return self.shape

  def __len__(self):
    return len(self.shape)

  def __repr__(self):
    return str(self.shape)

  # def __int__(self):
  #  return int(sum(self.shape))
