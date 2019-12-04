#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.utilities import SignalSpace, Range

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 15/09/2019
           """


def test1():
    acs = SignalSpace([Range(min_value=0, max_value=3, decimal_granularity=2)], ())
    print(acs, acs.low, acs.high, acs.decimal_granularity)


def test_sparsity():
    acs = SignalSpace([Range(min_value=0, max_value=3, decimal_granularity=0)], ())

    assert acs.is_sparse
