#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from typing import Sequence

from neodroid.utilities.spaces.range import Range
from neodroid.utilities.spaces.space import Space
from neodroid.utilities.transformations.encodings import signed_ternary_encoding

__author__ = "Christian Heider Nielsen"
__all__ = ["ActionSpace"]

import numpy


class ActionSpace(Space):
    def sample(self):
        actions = []
        for valid_input in self._ranges:
            sample = numpy.random.uniform(
                valid_input.min_unnorm, valid_input.max_unnorm, 1
            ).item()
            actions.append(numpy.round(sample, valid_input.decimal_granularity))
        return actions

    def validate(self, actions):
        for i in range(len(actions)):
            clipped = numpy.clip(
                actions[i], self._ranges[i].min_unnorm, self._ranges[i].max_unnorm
            )
            actions[i] = numpy.round(clipped, self._ranges[i].decimal_granularity)
        return actions

    def discrete_one_hot_sample(self):
        idx = numpy.random.randint(0, self.num_actuators)
        zeros = numpy.zeros(self.num_actuators)
        if len(self._ranges) > 0:
            val = numpy.random.random_integers(
                int(self._ranges[idx].min_unnorm), int(self._ranges[idx].max_unnorm), 1
            )
            zeros[idx] = val
        return zeros

    def discrete_sample(self):
        idx = numpy.random.randint(0, self.discrete_steps)
        return idx

    def one_hot_sample(self):

        idx = numpy.random.randint(0, self.num_actuators)
        zeros = numpy.zeros(self.num_actuators)
        if len(self._ranges) > 0:
            zeros[idx] = 1
        return zeros

    @property
    def num_actuators(self):
        return self.n


if __name__ == "__main__":
    acs = ActionSpace(
        [
            Range(min_value=0, max_value=3, decimal_granularity=2),
            Range(min_value=0, max_value=2, decimal_granularity=1),
        ]
    )
    print(
        acs, acs.low, acs.high, acs.decimal_granularity, acs.discrete_steps, acs.shape
    )

    acs = ActionSpace(
        [
            Range(min_value=0, max_value=3, decimal_granularity=2, normalised=False),
            Range(min_value=0, max_value=2, decimal_granularity=1, normalised=False),
        ]
    )
    print(
        acs,
        acs.low,
        acs.high,
        acs.decimal_granularity,
        acs.discrete_steps,
        acs.shape,
        acs.discrete_steps_shape,
    )

    acs = ActionSpace(
        [Range(min_value=0, max_value=1, decimal_granularity=0, normalised=False)]
    )
    print(
        acs,
        acs.low,
        acs.high,
        acs.decimal_granularity,
        acs.discrete_steps,
        acs.shape,
        acs.discrete_steps_shape,
    )
