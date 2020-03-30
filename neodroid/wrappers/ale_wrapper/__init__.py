#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"

from .ale_wrapper import NeodroidALEWrapper


def make(environment, configuration=None):
    return NeodroidALEWrapper(name=environment)
