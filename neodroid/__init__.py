#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from neodroid.environments import *
from neodroid.version import get_version

__author__ = 'cnheider'
__version__ = get_version()
__doc__ = r'''
.. module:: neodroid
   :platform: Unix, Windows
   :synopsis: An API for communicating with a Unity Game process.

.. moduleauthor:: Christian Heider Nielsen <christian.heider@alexandra.dk>


'''


def get_logo() -> str:
  with open('data/.ascii') as f:
    return f.read()


def draw_logo() -> None:
  print(get_logo())


if __name__ == '__main__':
  draw_logo()
