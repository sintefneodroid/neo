#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'
__version__ = None
'''
.. module:: neodroid
   :platform: Unix, Windows
   :synopsis: An API for communicating with a Unity Game process.

.. moduleauthor:: Christian Heider Nielsen <chrini13@student.aau.dk>


'''
import numpy as np

from .models import *
from .neodroid_environments import NeodroidEnvironments
# from .utilities import *
from .version import __version__


def make(environment, clones=0, *args, **kwargs):
  return NeodroidEnvironments(name=environment, clones=clones, *args, **kwargs)


def seed(seed):
  np.random.seed(seed)


def get_available_environments():
  return environments


@property
def environments():
  return 'All of them ;)'
