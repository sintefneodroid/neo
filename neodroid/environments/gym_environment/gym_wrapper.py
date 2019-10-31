#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from warnings import warn

from gym import Env

from neodroid.environments.unity_environment.single_unity_environment import SingleUnityEnvironment
from neodroid.utilities.spaces import ActionSpace, ObservationSpace, Range, SignalSpace
from neodroid.utilities.unity_specifications import EnvironmentSnapshot

__author__ = 'Christian Heider Nielsen'

import numpy
import gym


# warn(f"This module is deprecated in version {__version__}", DeprecationWarning)


class NeodroidGymEnvironment(SingleUnityEnvironment,
                             gym.Env):
  def __init__(self, render_interval: int = 0, **kwargs):
    super().__init__(**kwargs)
    self._render_interval = render_interval

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
    if self._last_valid_message:
      return self._last_valid_message.sensor(key)
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


class NeodroidVectorGymEnvironment(SingleUnityEnvironment,
                                   gym.Env):

  def __init__(self, render_interval: int = 0, **kwargs):
    super().__init__(**kwargs)
    self._render_interval = render_interval

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
      return (numpy.array([message.observables]),
              numpy.array([message.signal]),
              numpy.array([message.terminated]),
              numpy.array([message])
              )
    raise ValueError('Did not receive any message.')

  def reset(self, *args, **kwargs):
    message = super().reset(*args, **kwargs)
    if message:
      return numpy.array([message.observables])
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
  def __init__(self, environment: Env,
               render_interval: int = 0,
               min_signal=-1,
               max_signal=1):
    '''

    :param environment:
    '''
    self._env = environment
    self._render_interval = render_interval

  @property
  def signal_space(self) -> SignalSpace:
    '''

    :return:
    '''

    space = SignalSpace([Range(min_value=-float('inf'),
                               max_value=float('inf'),
                               decimal_granularity=9)])

    return space

  @property
  def observation_space(self) -> ObservationSpace:
    '''

    :return:
    '''

    if len(self._env.observation_space.shape) >= 1:
      aspc = self._env.observation_space
      space = ObservationSpace([Range(decimal_granularity=2,
                                      min_value=mn,
                                      max_value=mx)
                                for _, mn, mx in zip(range(
          self._env.observation_space.shape[0]),
          aspc.low,
          aspc.high)])
    else:
      space = ObservationSpace([Range(min_value=0,
                                      max_value=self._env.observation_space.n,
                                      decimal_granularity=0)])

    return space

  @property
  def action_space(self) -> ActionSpace:
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
    if isinstance(a, numpy.ndarray):
      a = a.tolist()

    observables, signal, terminated, *_ = self._env.step(a,
                                                         *args,
                                                         **kwargs)

    env_state = EnvironmentSnapshot.from_gym_like_out(observables, signal, terminated, None)

    return env_state

  def reset(self):
    observables = self._env.reset()

    env_state = EnvironmentSnapshot.from_gym_like_out(observables, 0, False, None)

    return env_state

  def __getattr__(self, item):
    return getattr(self._env, item)


if __name__ == '__main__':
  env = NeodroidGymWrapper(gym.make('CartPole-v1'))
  print(env.observation_space)
  print(env.action_space)
