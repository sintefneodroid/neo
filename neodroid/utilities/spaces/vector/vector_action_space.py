#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from neodroid.utilities.spaces.action_space import ActionSpace
from neodroid.utilities.spaces.range import Range

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 9/5/19
           """


class VectorActionSpace:
    def __init__(self, action_space: ActionSpace, num_env: int):
        self.action_space = action_space
        self.num_env = num_env

    def sample(self):
        return [self.action_space.sample() for _ in range(self.num_env)]

    def __getattr__(self, item):
        return getattr(self.action_space, item)

    def __repr__(self):
        return self.action_space.__repr__()
