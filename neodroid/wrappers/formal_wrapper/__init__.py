#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"

import numpy

from .formal_wrapper import NeodroidFormalWrapper


def make(environment_name, **kwargs):
    return NeodroidFormalWrapper(environment_name=environment_name, **kwargs)


def connect():
    return NeodroidFormalWrapper(connect_to_running=True)


def seed(s):
    numpy.random.random(s)
