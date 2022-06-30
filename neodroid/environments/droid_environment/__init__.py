#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""
           """

from warg import passes_kws_to

from .bullet_environment import *
from .godot_environment import *
from .unity import *


@passes_kws_to(DictUnityEnvironment.__init__)
def make_dict(
    environment_name: str = None, clones: int = 0, *args, **kwargs
) -> DictUnityEnvironment:
    _environments = DictUnityEnvironment(
        environment_name=environment_name, clones=clones, *args, **kwargs
    )
    return _environments


@passes_kws_to(DictUnityEnvironment.__init__)
def connect_dict(
    ip: str = "localhost", port: int = 6969, **kwargs
) -> DictUnityEnvironment:
    _environments = DictUnityEnvironment(
        connect_to_running=True, ip=ip, port=port, **kwargs
    )
    return _environments


@passes_kws_to(VectorUnityEnvironment.__init__)
def make_vector(
    environment_name: str = None, clones: int = 0, *args, **kwargs
) -> VectorUnityEnvironment:
    _environments = VectorUnityEnvironment(
        environment_name=environment_name, clones=clones, *args, **kwargs
    )
    return _environments


@passes_kws_to(VectorUnityEnvironment.__init__)
def connect_vector(
    ip: str = "localhost", port: int = 6969, **kwargs
) -> VectorUnityEnvironment:
    _environments = VectorUnityEnvironment(
        connect_to_running=True, ip=ip, port=port, **kwargs
    )
    return _environments
