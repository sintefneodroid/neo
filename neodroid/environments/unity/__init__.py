#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .unity_environment import UnityEnvironment

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''
           '''


def make(environment_name: str = None, clones=0, *args, **kwargs) -> UnityEnvironment:
  _environments = UnityEnvironment(environment_name=environment_name,
                                   clones=clones,
                                   *args,
                                   **kwargs)
  return _environments


def connect(ip='localhost', port=6969, **kwargs) -> UnityEnvironment:
  _environments = UnityEnvironment(connect_to_running=True,
                                   ip=ip,
                                   port=port,
                                   **kwargs)
  return _environments


from .single_unity_environment import *
from .unity_environment import *
from .vector_unity_environment import *
from .batched_unity_environments import *
