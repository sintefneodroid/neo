#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sized, Sequence

from neodroid.utilities.spaces import Space

from neodroid.utilities.spaces import Range

__author__ = 'Christian Heider Nielsen'


class ObservationSpace(Space):

  def parse_observation_space(self, observations_spaces: Sequence[Range], sensor_names: Sequence[str]):
    self._ranges = observations_spaces
    self._names = sensor_names

  def parse_gym_space(self, ob):
    pass

  @property
  def space(self) -> Sequence:
    return self.continuous_shape


if __name__ == '__main__':
  acs = ObservationSpace([Range()], ())
  print(acs)
