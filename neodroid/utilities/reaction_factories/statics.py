#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import Iterable

from neodroid.utilities import ActionSpace, ObservationSpace, Range

__author__ = 'cnheider'


def flattened_observation(message):
  # flat = np.array([np.hstack([obs.observation_value]).flatten() for obs in message.observers.values() if
  # obs.observation_value is not None and type(obs.observation_value) is not _io.BytesIO])
  # flatter = np.hstack(flat).flatten()
  # flatter = np.hstack(flatter).flatten()
  # flatest = np.nan_to_num(flatter).tolist()
  obs = message.observables
  return obs


def construct_action_space(environment_description):
  motion_spaces = []
  for actor in environment_description.actors.values():
    for motor in actor.motors.values():
      motion_spaces.append(motor.motion_space)

  action_space = ActionSpace()
  action_space.parse_action_space(motion_spaces)
  return action_space


def construct_observation_space(environment):
  observation_spaces = []
  observers = environment.observers.values()
  for observer in observers:
    if isinstance(observer.observation_space, Iterable):
      for range in observer.observation_space:
        observation_spaces.append(range)
    else:
      observation_spaces.append(observer.observation_space)

  observation_space = ObservationSpace()
  observation_space.parse_observation_space(observation_spaces)
  return observation_space
