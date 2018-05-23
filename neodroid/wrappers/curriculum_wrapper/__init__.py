#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

import numpy as np

from .curriculum_wrapper import NeodroidCurriculumWrapper


def make(environment, **kwargs):
  return NeodroidCurriculumWrapper(name=environment, **kwargs)


def seed(seed):
  np.random.random(seed)
