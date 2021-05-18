#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 17-05-2021
           """

from neodroid.utilities.specifications.unity_specifications.environment_description import (
    EnvironmentDescription,
)


__all__ = ["VectorEnvironmentDescription"]


class VectorEnvironmentDescription:
    def __init__(self, environment_description: EnvironmentDescription, num_env: int):
        self.environment_description = environment_description
        self.num_env = num_env

    def __getattr__(self, item):
        return getattr(self.environment_description, item)

    def __repr__(self):
        return self.environment_description.__repr__()
