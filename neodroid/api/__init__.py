#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from neodroid.api.neodroid_environments import NeodroidEnvironment

__author__ = 'cnheider'
__doc__ = ''

_environments = None


def draw_logo():
  with open('data/.ascii') as f:
    print(f.read())


def make(environment_name='', clones=0, *args, **kwargs):
  global _environments
  _environments = NeodroidEnvironment(environment_name=environment_name, clones=clones, *args, **kwargs)
  return _environments


def connect(ip='localhost', port=6969, *args, **kwargs):
  global _environments
  _environments = NeodroidEnvironment(ip=ip, port=port, connect_to_running=True, *args, **kwargs)
  return _environments


def seed(random_seed):
  import numpy as np
  np.random.seed(random_seed)


def get_available_environments():
  return environments


@property
def environments():
  return _environments
