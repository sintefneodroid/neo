#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.models.space import Space

__author__ = 'cnheider'


class ObservationSpace(Space):

  @property
  def shape(self):
    return [len(self._state)]

  def parse_observation_space(self, state):
    self._state = state
