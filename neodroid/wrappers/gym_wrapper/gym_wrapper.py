#!/usr/bin/env python3
# coding=utf-8
__author__ = 'cnheider'

import gym
import numpy as np

from neodroid import NeodroidEnvironment
from neodroid.utilities.statics import flattened_observation


class NeodroidGymWrapper(NeodroidEnvironment):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def step(self, action, *args, **kwargs):
    # action = action.flatten()
    message = super(NeodroidGymWrapper, self).react(action, *args, **kwargs)
    if message:
      return (np.array(flattened_observation(message)),
              message.signal,
              message.terminated, message)
    return None, None, None, None

  def reset(self, *args, **kwargs):
    message = super(NeodroidGymWrapper, self).reset(*args, **kwargs)
    if message:
      return np.array(flattened_observation(message))
    return None

  def render(self, *args, **kwargs):
    pass

  def sensor(self, key):
    if self._last_message:
      return self._last_message.observer(key)
    return None

  def __next__(self):
    if not self._connected_to_server:
      raise StopIteration
    return self.step()


class NormalizedActions(gym.ActionWrapper):

  def _action(self, action):
    action = (action + 1) / 2  # [-1, 1] => [0, 1]
    action *= (self.action_space.high - self.action_space.low)
    action += self.action_space.low
    return action

  def _reverse_action(self, action):
    action -= self.action_space.low
    action /= (self.action_space.high - self.action_space.low)
    action = action * 2 - 1
    return action
