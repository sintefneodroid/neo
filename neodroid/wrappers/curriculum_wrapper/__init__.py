#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"

import numpy

from .curriculum_wrapper import NeodroidCurriculumWrapper


def make(environment, **kwargs):
    return NeodroidCurriculumWrapper(name=environment, **kwargs)


def seed(seed):
    numpy.random.random(seed)
