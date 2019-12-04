#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest

from neodroid.utilities.spaces import Range

__author__ = "Christian Heider Nielsen"


@pytest.mark.parametrize(
    ("min", "max", "dec", "norm"),
    [(0, 0, 0, False), (1, 2, 1, False), (-1, 2, 1, False)],
)
def test_space_construction(min, max, dec, norm):
    space = Range(
        min_value=min, max_value=max, decimal_granularity=dec, normalised=norm
    )
    assert space.min == min
    assert space.max == max
    assert space.min_unnorm == min
    assert space.max_unnorm == max
    assert space.decimal_granularity == dec
    assert space.normalised == norm
