#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.models import Range

__author__ = 'cnheider'

def inc(x):
  return x + 1

def test_answer():
  assert inc(4) == 5

def test_space():
  space = Range(1, -1, 1)
  assert space.min_value != 0
