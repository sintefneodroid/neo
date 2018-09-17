#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from neodroid.wrappers.gym_wrapper.gym_wrapper import NeodroidGymWrapper

__author__ = 'cnheider'

import numpy as np


def make(environment_name, **kwargs):
  return NeodroidGymWrapper(environment_name=environment_name, **kwargs)


def seed(seed):
  np.random.random(seed)
