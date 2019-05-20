#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .gym_wrapper import *

__author__ = 'cnheider'

import numpy as np


def make(environment_name, **kwargs):
  return NeodroidVectorGymWrapper(environment_name=environment_name, **kwargs)


def seed(seed):
  np.random.random(seed)
