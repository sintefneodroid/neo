#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.utilities import Range

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 15/09/2019
           """


def test_1():
    r = Range(min_value=0, max_value=5, decimal_granularity=2)
    print(r, r.sample())


def test_11():
    r = Range(min_value=0, max_value=2, decimal_granularity=0, normalised=False)
    print(r.span, r.sample(), r.discrete_steps, r.max, r.min)

    a = 2
    assert a == r.denormalise(r.normalise(a))
