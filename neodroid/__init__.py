#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from neodroid.version import get_version

from .api import *
from .api_wrappers import *

__author__ = 'cnheider'
__version__ = get_version()
__doc__ = r'''
.. module:: neodroid
   :platform: Unix, Windows
   :synopsis: An API for communicating with a Unity Game process.

.. moduleauthor:: Christian Heider Nielsen <christian.heider@alexandra.dk>


'''
