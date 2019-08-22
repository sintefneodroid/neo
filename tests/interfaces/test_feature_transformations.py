#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.interfaces import Range

__author__ = 'cnheider'


def test_space_construction():
  space = Range(min_value=-1, max_value=1, decimal_granularity=1)
  assert space.min_value != 0
  assert space.max_value != 0
  assert space.decimal_granularity != 0
