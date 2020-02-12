#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from warg import passes_kws_to
from .unity_environment import UnityEnvironment

__author__ = "Christian Heider Nielsen"
__doc__ = r"""
           """


@passes_kws_to(UnityEnvironment.__init__)
def make(
    environment_name: str = None, clones: int = 0, *args, **kwargs
) -> UnityEnvironment:
    _environments = UnityEnvironment(
        environment_name=environment_name, clones=clones, *args, **kwargs
    )
    return _environments


@passes_kws_to(UnityEnvironment.__init__)
def connect(ip: str = "localhost", port: int = 6969, **kwargs) -> UnityEnvironment:
    _environments = UnityEnvironment(
        connect_to_running=True, ip=ip, port=port, **kwargs
    )
    return _environments


from neodroid.environments.unity_environment.deprecated.single_unity_environment import *
from .unity_environment import *
from .vector_unity_environment import *
from neodroid.environments.unity_environment.deprecated.batched_unity_environments import *
