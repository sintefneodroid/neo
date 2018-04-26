#!/usr/bin/env python3
# coding=utf-8
__author__ = 'cnheider'
__version__ = None
'''
.. module:: neodroid
   :platform: Unix, Windows
   :synopsis: An API for communicating with a Unity Game process.

.. moduleauthor:: Christian Heider Nielsen <chrini13@student.aau.dk>


'''
import numpy as np

from .neodroid_environment import NeodroidEnvironment
from .version import __version__


def make(environment, *args, **kwargs):
  return NeodroidEnvironment(name=environment, *args, **kwargs)


def seed(seed):
  np.random.seed(seed)


def get_available_environments():
  return environments


@property
def environments():
  return 'All of them ;)'
