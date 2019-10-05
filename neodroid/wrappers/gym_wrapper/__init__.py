#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .gym_wrapper import *

__author__ = 'Christian Heider Nielsen'

import numpy


def make(environment_name, **kwargs):
  return NeodroidVectorGymEnvironment(environment_name=environment_name, **kwargs)


def seed(seed):
  numpy.random.random(seed)
