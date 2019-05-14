#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from warnings import warn

from neodroid.utilities import flattened_observation
from neodroid.version import __version__
from neodroid.wrappers.experimental.single_environment_wrapper import SingleEnvironmentWrapper

__author__ = 'cnheider'

import numpy as np
import gym

warn(f"This module is deprecated in version {__version__}", DeprecationWarning)


class NeodroidGymWrapper(SingleEnvironmentWrapper,
                         gym.Env):

  def step(self, action=None, *args, **kwargs):
    # action = action.flatten()
    message = super().react(action[0], **kwargs)
    if message:
      return (flattened_observation(message),
              message.signal,
              message.terminated,
              message
              )
    raise ValueError('Did not receive any message.')

  def reset(self, *args, **kwargs):
    message = super().reset(*args, **kwargs)
    if message:
      return flattened_observation(message)
    return None

  def render(self, *args, **kwargs):
    pass

  def sensor(self, key):
    if self._last_message:
      return self._sensor(key)
    warn('No message available')
    return None

  def __next__(self):
    if not self._is_connected_to_server:
      raise ValueError('Not connected to a server.')
    return self.step()

  @property
  def metadata(self):
    return {'render.modes':['rgb_array']}

  @property
  def reward_range(self):
    return -float('inf'), float('inf')

  @property
  def spec(self):
    return None

  @property
  def action_space(self):
    return self._action_space

  @property
  def observation_space(self):
    return self._observation_space


class NeodroidVectorGymWrapper(SingleEnvironmentWrapper,
                               gym.Env):

  def step(self, action=None, *args, **kwargs):
    # action = action.flatten()
    message = super().react(action[0], **kwargs)
    if message:
      return (np.array([flattened_observation(message)]),
              np.array([message.signal]),
              np.array([message.terminated]),
              np.array([message])
              )
    raise ValueError('Did not receive any message.')

  def reset(self, *args, **kwargs):
    message = super().reset(*args, **kwargs)
    if message:
      return np.array([flattened_observation(message)])
    return None

  def render(self, *args, **kwargs):
    pass

  def sensor(self, key):
    if self._last_message:
      return self._sensor(key)
    warn('No message available')
    return None

  def __next__(self):
    if not self._is_connected_to_server:
      raise ValueError('Not connected to a server.')
    return self.step()

  @property
  def metadata(self):
    return {'render.modes':['rgb_array']}

  @property
  def reward_range(self):
    return -float('inf'), float('inf')

  @property
  def spec(self):
    return None

  @property
  def action_space(self):
    return self._action_space

  @property
  def observation_space(self):
    return self._observation_space


class NeodroidWrapper:
  def __init__(self, env):
    self.env = env

  def react(self, a, *args, **kwargs):
    if isinstance(a, np.ndarray):
      a = a.tolist()

    observables, signal, terminated, *_ = self.env.step(a, *args, **kwargs)

    return observables, signal, terminated

  def reset(self):
    return self.env.reset()

  def __getattr__(self, item):
    return getattr(self.env, item)


if __name__ == '__main__':
  NeodroidVectorGymWrapper()
