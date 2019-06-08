#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from neodroid.api.neodroid_environments import NeodroidEnvironment

__author__ = 'cnheider'
__doc__ = ''


def draw_logo():
  with open('data/.ascii') as f:
    print(f.read())


def make(environment_name='', clones=0, *args, **kwargs):
  _environments = NeodroidEnvironment(environment_name=environment_name, clones=clones, *args, **kwargs)
  return _environments


def seed(random_seed):
  import numpy as np
  np.random.seed(random_seed)
