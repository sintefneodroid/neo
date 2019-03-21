#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.models.range import Range
from neodroid.models.space import Space

__author__ = 'cnheider'


class ObservationSpace(Space):

  @property
  def ranges(self):
    return self._observation_spaces

  @property
  def shape(self):
    return [self.__len__()]

  def __len__(self):
    return len(self._observation_spaces)

  def parse_observation_space(self, observations_spaces):
    self._observation_spaces = observations_spaces
