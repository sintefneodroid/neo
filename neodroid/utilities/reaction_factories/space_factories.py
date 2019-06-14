#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import Sequence

from neodroid.utilities import ActionSpace, ObservationSpace

__author__ = 'cnheider'


def construct_action_space(environment_description):
  motion_spaces = []
  for actor in environment_description.actors.values():
    for motor in actor.actuators.values():
      motion_spaces.append(motor.motion_space)

  action_space = ActionSpace([])
  action_space.parse_action_space(motion_spaces)
  return action_space


def construct_observation_space(environment):
  observation_spaces = []
  observers = environment.observers.values()
  for observer in observers:
    if isinstance(observer.space, Sequence):
      for r in observer.space:
        observation_spaces.append(r)
    else:
      observation_spaces.append(observer.space)

  observation_space = ObservationSpace([])
  observation_space.parse_observation_space(observation_spaces)
  return observation_space
