# !/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cnheider'

import pytest


def inc(x):
  return x + 1


def test_answer():
  assert inc(3) == 5


with pytest.raises(AssertionError):
  raise AssertionError

with pytest.raises(ValueError):
  raise ValueError
