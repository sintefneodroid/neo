#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.utilities.launcher.download_utilities.download_environment import available_environments

__author__ = 'cnheider'

from .environment_launcher import *


def get_available_environments():
  return available_environments()
