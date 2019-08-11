#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from warnings import warn

from gym import Env

from neodroid.wrappers.single_environment import SingleEnvironment
from neodroid.interfaces.spaces import ActionSpace, ObservationSpace, Range
from neodroid.interfaces.specifications import EnvironmentSnapshot

__author__ = 'cnheider'

import numpy as np
import gym


# warn(f"This module is deprecated in version {__version__}", DeprecationWarning)


class NeodroidGymEnvironment(SingleEnvironment,
                             gym.Env):

  def step(self, action=None, *args, **kwargs):
    '''

    :param action:
    :param args:
    :param kwargs:
    :return:
    '''
    # action = action.flatten()
    message = super().react(action, **kwargs)
    if message:
      return (message.observables,
              message.signal,
              message.terminated,
              message
              )
    raise ValueError('Did not receive any message.')

  def reset(self, *args, **kwargs):
    """

    :param args:
    :param kwargs:
    :return:
    """
    message = super().reset(*args, **kwargs)
    if message:
      return message.observables
    return None

  def render(self, *args, **kwargs):
    pass

  def sensor(self, key, **kwargs):
    if self._last_message:
      return self._last_message.sensor(key)
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


class NeodroidVectorGymEnvironment(SingleEnvironment,
                                   gym.Env):

  def step(self, action=None, *args, **kwargs):
    '''

    :param action:
    :param args:
    :param kwargs:
    :return:
    '''
    # action = action.flatten()
    message = super().react(action[0], **kwargs)
    if message:
      return (np.array([message.observables]),
              np.array([message.signal]),
              np.array([message.terminated]),
              np.array([message])
              )
    raise ValueError('Did not receive any message.')

  def reset(self, *args, **kwargs):
    message = super().reset(*args, **kwargs)
    if message:
      return np.array([message.observables])
    return None

  def render(self, *args, **kwargs):
    pass

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


class NeodroidGymWrapper:
  def __init__(self, environment: Env):
    '''

    :param environment:
    '''
    self._env = environment

  @property
  def observation_space(self):
    '''

    :return:
    '''

    if len(self._env.observation_space.shape) >= 1:
      aspc = self._env.observation_space
      space = ObservationSpace([Range(decimal_granularity=2,
                                      min_value=mn,
                                      max_value=mx)
                                for _, mn, mx in zip(range(
            self._env.observation_space.shape[0]), aspc.low, aspc.high)])
    else:
      space = ObservationSpace([Range(min_value=0,
                                      max_value=self._env.observation_space.n,
                                      decimal_granularity=0)])

    return space

  @property
  def action_space(self):
    '''

    :return:
    '''

    if len(self._env.action_space.shape) >= 1:
      aspc = self._env.action_space
      space = ActionSpace([Range(decimal_granularity=2,
                                 min_value=mn,
                                 max_value=mx
                                 )
                           for _, mn, mx in zip(range(self._env.action_space.shape[0]), aspc.low, aspc.high)])
    else:
      space = ActionSpace([Range(min_value=0,
                                 max_value=self._env.action_space.n,
                                 decimal_granularity=0)])

    return space

  def react(self, a, *args, **kwargs):
    if isinstance(a, np.ndarray):
      a = a.tolist()

    observables, signal, terminated, *_ = self._env.step(a, *args, **kwargs)

    env_state = EnvironmentSnapshot(None)
    env_state._observables = observables
    env_state._signal = signal
    env_state._terminated = terminated

    return env_state

  def reset(self):
    observables = self._env.reset()

    env_state = EnvironmentSnapshot(None)
    env_state._observables = observables

    return env_state

  def __getattr__(self, item):
    return getattr(self._env, item)


if __name__ == '__main__':
  env = NeodroidGymWrapper(gym.make('CartPole-v1'))
  print(env.observation_space)
  print(env.action_space)
