#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.models import Range

__author__ = 'cnheider'


def test_space():
  space = Range(min_value=-1, max_value=1, decimal_granularity=1)
  assert space.min_value != 0
