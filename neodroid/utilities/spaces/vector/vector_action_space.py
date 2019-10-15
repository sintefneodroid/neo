#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.utilities import ActionSpace, Range, Sequence

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 9/5/19
           '''


class VectorActionSpace(ActionSpace):
  def __init__(self, ranges: Sequence[Range], num_env):
    super().__init__(ranges)
    self.num_env = num_env

  def sample(self):
    return [super(ActionSpace, self).sample() for _ in range(self.num_env)]
