#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from warnings import warn

import numpy as np

from neodroid.environments import NeodroidEnvironment


from neodroid.factories.multi_reaction_factory import (maybe_infer_multi_motion_reaction,
                                                       maybe_infer_multi_configuration_reaction,
                                                       )
from neodroid.interfaces.spaces import (ActionSpace,
                                        ObservationSpace,
                                        Range,
                                        SignalSpace,
                                        EnvironmentDescription,
                                        )
from neodroid.interfaces.specifications import EnvironmentSnapshot, Reaction, ReactionParameters

__author__ = 'cnheider'


class VectorEnvironment(NeodroidEnvironment):

  def __next__(self):
    if not self._is_connected_to_server:
      return
    return self.react()

  def react(self,
            input_reactions=None,
            *,
            parameters: ReactionParameters = None,
            normalise: bool = False,
            **kwargs):
    if not isinstance(input_reactions, Reaction):
      input_reactions = maybe_infer_multi_motion_reaction(input_reactions=input_reactions,
                                                          normalise=normalise,
                                                          descriptions=self._description,
                                                          action_space=self.action_space
                                                          )
    if parameters is not None:
      input_reactions.parameters = parameters

    env_states = super().react(input_reactions=input_reactions, **kwargs)

    envs = list(env_states.values())
    e = EnvironmentSnapshot(None)
    e._observables = [e_.observables for e_ in envs]
    e._signal = [e_.signal for e_ in envs]
    e._terminated = [e_.terminated for e_ in envs]

    return e

  def reset(self,
            input_reactions=None,
            state=None,
            on_reset_callback:callable=None):

    input_reactions = maybe_infer_multi_configuration_reaction(input_reactions=input_reactions,
                                                               description=self._description
                                                               )
    #if state:
    #  input_reaction.unobservables = state.unobservables

    input_reactions = [input_reactions]
    new_states = super().reset(input_reactions)

    envs = list(new_states.values())
    e = EnvironmentSnapshot(None)
    e._observables = [e_.observables for e_ in envs]
    e._signal = [e_.signal for e_ in envs]
    e._terminated = [e_.terminated for e_ in envs]

    return e

  def configure(self, *args, **kwargs):
    message = self.reset(*args, **kwargs)
    if message:
      return message
    return None

  def describe(self, *args, **kwargs):
    new_states = super().describe(*args, **kwargs)
    envs = list(new_states.values())
    e = EnvironmentSnapshot(None)
    e._observables = [e_.observables for e_ in envs]
    e._signal = [e_.signal for e_ in envs]
    e._terminated = [e_.terminated for e_ in envs]

    return e
  '''

  def signal_space(self) -> SignalSpace:
    pass

  def description(self) -> EnvironmentDescription:
    pass
'''

  def sensor(self, name:str, *args, **kwargs):

    envs = list(self._last_message.values())

    observer = []
    for e in envs:
      o = e.sensor(name)
      if not o:
        warn('Sensor was not found!')
      observer.append(o)
    return observer


class VectorWrapper:
  def __init__(self, env: NeodroidEnvironment):
    '''

    :param env:
    '''
    self._env = env

  @property
  def observation_space(self)-> ObservationSpace:
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
      _output_shape = ActionSpace([Range(min_value=0,
                                         max_value=next(iter(self._env.action_space.values())).n,
                                         decimal_granularity=0)])

    return _output_shape

  def react(self, a, *args, **kwargs):
    if isinstance(a, np.ndarray):
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

  env = VectorEnvironment(environment_name=proc_args.ENVIRONMENT_NAME,
                          connect_to_running=proc_args.CONNECT_TO_RUNNING)

  observation_session = tqdm(env, leave=False)
  for environment_state in observation_session:
    if environment_state.terminated:
      print(f'Interrupted {environment_state.signal}')
      env.reset()
