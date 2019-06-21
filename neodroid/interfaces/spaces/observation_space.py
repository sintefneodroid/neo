#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import Sequence

from neodroid.interfaces.environment_models import EnvironmentDescription, Range, Space

__author__ = 'cnheider'


class ObservationSpace(Space):

  def parse_observation_space(self, observations_spaces, sensor_names):
    self._ranges = observations_spaces
    self._names = sensor_names

  def parse_gym_space(self, ob):
    pass

  def space(self):
    self.continuous_shape()

  @staticmethod
  def from_environment_description(environment_description: EnvironmentDescription):
    sensor_names = environment_description.sensors.keys()
    observation_spaces = []
    observers = environment_description.sensors.values()
    for observer in observers:
      if isinstance(observer.space, Sequence):
        for r in observer.space:
          observation_spaces.append(r)
      else:
        observation_spaces.append(observer.space)

    return ObservationSpace(observation_spaces, sensor_names)


if __name__ == '__main__':
  acs = ObservationSpace([Range()], ())
  print(acs)
