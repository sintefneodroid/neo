#!/usr/bin/env python3
# coding=utf-8
__author__ = 'cnheider'

import numpy as np

from .formal_wrapper import NeodroidFormalWrapper


def make(environment, **kwargs):
  return NeodroidFormalWrapper(name=environment, **kwargs)

def seed(seed):
  np.random.random(seed)
