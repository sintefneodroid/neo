#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum, IntEnum

__author__ = 'cnheider'
__doc__ = ''


class VerbosityLevel(IntEnum):
  Nothing = 0
  Errors = 1
  Warnings = 2
  Information = 3
