#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.neodroid_utilities import ActionSpace, ObservationSpace, Range

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
  if len(observers)>0:
    for observer in observers:
      observation_spaces.append(observer.observation_space)
  else:
    a = len(environment.observables)
    for i in range(a):
      observation_spaces.append(Range())

  observation_space = ObservationSpace()
  observation_space.parse_observation_space(observation_spaces)
  return observation_space
