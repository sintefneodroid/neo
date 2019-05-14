#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.models.range import Range
from neodroid.models.space import Space

__author__ = 'cnheider'


class ObservationSpace(Space):

  def parse_observation_space(self, observations_spaces):
    self._ranges = observations_spaces


if __name__ == '__main__':
  acs = ObservationSpace([Range()])
  print(acs)
