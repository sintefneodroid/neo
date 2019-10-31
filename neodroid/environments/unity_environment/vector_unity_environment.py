#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy

from neodroid.environments.unity_environment import UnityEnvironment
from neodroid.factories.configuration_reactions import verify_configuration_reactions
from neodroid.factories.motion_reactions import (verify_motion_reactions
                                                 )
from neodroid.utilities.spaces import (ActionSpace,
                                       ObservationSpace,
                                       Range,
                                       SignalSpace,
                                       )
from neodroid.utilities.spaces.vector.vector_action_space import VectorActionSpace
from neodroid.utilities.unity_specifications import (EnvironmentDescription,
                                                     EnvironmentSnapshot,
                                                     Reaction,
                                                     ReactionParameters,
                                                     )

__author__ = 'Christian Heider Nielsen'


class VectorUnityEnvironment(UnityEnvironment):

  def __next__(self):
    if not self._is_connected_to_server:
      return
    return self.react()

  def react(self,
            input_reactions=None,
            *,
            parameters: ReactionParameters = None,
            **kwargs) -> EnvironmentSnapshot:
    if not isinstance(input_reactions, Reaction):
      input_reactions = verify_motion_reactions(input_reactions=input_reactions,
                                                environment_descriptions=self._description
                                                )
    if parameters is not None:
      input_reactions.parameters = parameters

    env_states = super().react(input_reactions=input_reactions, **kwargs)

    envs = list(env_states.values())
    e = EnvironmentSnapshot.from_gym_like_out([e_.observables for e_ in envs],
                                              [e_.signal for e_ in envs],
                                              [e_.terminated for e_ in envs],
                                              None)
    return e

  def reset(self,
            input_reactions=None,
            state=None,
            on_reset_callback: callable = None) -> EnvironmentSnapshot:

    input_reactions = verify_configuration_reactions(input_reactions=input_reactions,
                                                     environment_descriptions=self._description
                                                     )
    # if state:
    #  input_reaction.unobservables = state.unobservables

    new_states = super().reset(input_reactions=input_reactions)

    envs = list(new_states.values())
    e = EnvironmentSnapshot.from_gym_like_out([e_.observables for e_ in envs],
                                              [e_.signal for e_ in envs],
                                              [e_.terminated for e_ in envs],
                                              None)

    return e

  def configure(self, *args, **kwargs):
    return self.reset(*args, **kwargs)

  @property
  def action_space(self) -> VectorActionSpace:
    while not self._action_space:
      self.describe()

    ev = next(iter(self._action_space.values()))
    _output_shape = VectorActionSpace(ev.ranges,
                                      len(self._action_space.values()))
    return _output_shape

  @property
  def description(self) -> EnvironmentDescription:
    while not self._description:
      self.describe()
    return next(iter(self._description.values()))

  @property
  def observation_space(self) -> ObservationSpace:
    while not self._observation_space:
      self.describe()
    return next(iter(self._observation_space.values()))

  @property
  def signal_space(self) -> SignalSpace:
    while not self._signal_space:
      self.describe()
    return next(iter(self._signal_space.values()))

  def describe(self, *args, **kwargs):
    new_states = super().describe(*args, **kwargs)
    envs = list(new_states.values())
    e = EnvironmentSnapshot.from_gym_like_out([e_.observables for e_ in envs],
                                              [e_.signal for e_ in envs],
                                              [e_.terminated for e_ in envs],
                                              None)

    return e

  '''

  def signal_space(self) -> SignalSpace:
    pass

  def description(self) -> EnvironmentDescription:
    pass
'''


class VectorWrapper:
  def __init__(self, env: UnityEnvironment):
    '''

    :param env:
    '''
    self._env = env

  @property
  def observation_space(self) -> ObservationSpace:
    '''

    :return:
    '''
    _input_shape = None

    if len(next(iter(self._env._observation_space.values())).shape) >= 1:
      _input_shape = next(iter(self._env._observation_space.values()))
    else:
      _input_shape = ObservationSpace([Range(min_value=0,
                                             max_value=next(iter(self._env._observation_space.values())).n,
                                             decimal_granularity=0)])

    return _input_shape

  @property
  def action_space(self) -> ActionSpace:
    '''

    :return:
    '''
    _output_shape = None

    if len(next(iter(self._env.action_space.values())).shape) >= 1:
      _output_shape = next(iter(self._env.action_space.values()))
    else:
      _output_shape = VectorActionSpace([Range(min_value=0,
                                               max_value=next(iter(self._env.action_space.values())).n,
                                               decimal_granularity=0)], len(self._env.action_space.values()))

    return _output_shape

  def react(self, a, *args, **kwargs):
    if isinstance(a, numpy.ndarray):
      a = a.tolist()

    info = self._env.react(a, *args, **kwargs)

    info = next(iter(info.values()))

    return info

  def reset(self):
    info = self._env.reset()

    info = next(iter(info.values()))

    return info

  def __getattr__(self, item):
    return getattr(self._env, item)


if __name__ == '__main__':
  import argparse
  from tqdm import tqdm

  parser = argparse.ArgumentParser(description='Single environment wrapper')
  parser.add_argument('--ENVIRONMENT_NAME',
                      type=str,
                      default='grd',
                      metavar='ENVIRONMENT_NAME',
                      help='name of the environment to run',
                      )
  parser.add_argument('--CONNECT_TO_RUNNING',
                      '-C',
                      action='store_true',
                      default=True,
                      help='Connect to already running environment instead of starting another instance')
  proc_args = parser.parse_args()

  env = VectorUnityEnvironment(environment_name=proc_args.ENVIRONMENT_NAME,
                               connect_to_running=proc_args.CONNECT_TO_RUNNING)

  observation_session = tqdm(env, leave=False)
  for environment_state in observation_session:
    if environment_state.terminated:
      print(f'Interrupted {environment_state.signal}')
      env.reset()
