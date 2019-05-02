#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.neodroid_environments import NeodroidEnvironment

__author__ = 'cnheider'


class BatchedNeodroidEnvironment(NeodroidEnvironment):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self._resets = []

  def _reset(self, resets=None, **kwargs):
    self._resets = resets
    return self._resets

  def _react(self, reactions=None, **kwargs):

    if self._resets and len(self._resets) > 0:
      i = 0
      for reset in self._resets:
        reactions[i].parameters.reset = reset
        i += 1
      self._resets = []

    environment_states = super()._react(input_reactions=reactions)

    observables = [environment_state.observables for environment_state in environment_states.values()]
    signals = [environment_state.signal for environment_state in environment_states.values()]
    terminated = [environment_state.terminated for environment_state in environment_states.values()]

    return observables, signals, terminated, environment_states


if __name__ == '__main__':
  import argparse
  from tqdm import tqdm

  parser = argparse.ArgumentParser(description='Batched Neodroid Environments')
  parser.add_argument(
      '--ENVIRONMENT_NAME',
      type=str,
      default='mab',
      metavar='ENVIRONMENT_NAME',
      help='name of the environment to run',
      )
  parser.add_argument(
      '--CONNECT_TO_RUNNING',
      '-C',
      action='store_true',
      default=True,
      help='Connect to already running environment instead of starting another instance')
  args = parser.parse_args()

  env = NeodroidEnvironment(name=args.ENVIRONMENT_NAME, connect_to_running=args.CONNECT_TO_RUNNING)

  observation_session = tqdm(env, leave=False)
  i = 0
  for environment_state in observation_session:
    first_environment_state = list(environment_state.values())[0]
    i += 1
    if first_environment_state.terminated:
      print(f'Interrupted, local frame number: {i}, remote:{first_environment_state.frame_number}')
      env.reset()
      i = 0
