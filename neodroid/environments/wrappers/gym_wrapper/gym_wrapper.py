#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from warnings import warn

from gym import Env

from neodroid.environments.wrappers.single_environment import SingleEnvironment
from neodroid.interfaces.environment_models import EnvironmentSnapshot
from neodroid.interfaces.spaces import ActionSpace, ObservationSpace, Range
from trolls import SubProcessEnvironments

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
  def __init__(self, env:Env):
    '''

    :param env:
    '''
    self._env = env

  @property
  def observation_space(self):
    '''

    :return:
    '''
    _input_shape = None

    if len(self._env.observation_space.shape) >= 1:
      _input_shape = ObservationSpace([Range(decimal_granularity=2) for _ in range(
          self._env.observation_space.shape[0])])
    else:
      _input_shape = ObservationSpace([Range(min_value=0,
                                         max_value=self._env.observation_space.n,
                                         decimal_granularity=0)])

    return _input_shape

  @property
  def action_space(self):
    '''

    :return:
    '''
    _output_shape = None

    if len(self._env.action_space.shape) >= 1:
      _output_shape = ActionSpace([Range(decimal_granularity=2) for _ in range(
          self._env.action_space.shape[0])])
    else:
      _output_shape = ActionSpace([Range(min_value=0,
                                         max_value=self._env.action_space.n,
                                         decimal_granularity=0)])

    return _output_shape

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
