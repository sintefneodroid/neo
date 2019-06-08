#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

from .curriculum_wrapper import *
from .formal_wrapper import *
from .gym_wrapper import *
from .observation_wrapper import *


def connect(ip='localhost', port=6969, *args, **kwargs):
  return SingleEnvironmentWrapper(ip=ip, port=port, connect_to_running=True, *args, **kwargs)
