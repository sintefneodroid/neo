#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math

import numpy

__author__ = "Christian Heider Nielsen"

__all__ = ["Range"]


class Range:
    """

"""

    def __init__(
        self, *, min_value=0, max_value=0, decimal_granularity=0, normalised=True
    ):
        """

:param min_value:
:param max_value:
:param decimal_granularity:
:param normalised:
"""
        assert max_value >= min_value
        assert decimal_granularity >= 0

        self._normalised = normalised
        self._decimal_granularity = decimal_granularity

        self._min_value = min_value
        self._max_value = max_value

    @property
    def normalised(self) -> bool:
        """
Indicates whether the action space span is zero-one normalised
:return:
"""
        return self._normalised

    @property
    def decimal_granularity(self) -> int:
        return self._decimal_granularity

    @property
    def min_unnorm(self) -> float:
        return self._min_value

    @property
    def min(self) -> float:
        if self.normalised:
            return 0
        return self.min_unnorm

    @property
    def max_unnorm(self) -> float:
        return self._max_value

    @property
    def max(self) -> float:
        if self.normalised:
            return 1
        return self.max_unnorm

    @property
    def discrete_step_size(self) -> float:
        return 1 / numpy.power(10, self.decimal_granularity)

    @property
    def span_unnorm(self) -> float:
        return self.max_unnorm - self.min_unnorm

    @property
    def span(self) -> float:
        if self.normalised:
            return 1
        return self.span_unnorm

    @property
    def discrete_steps(self) -> int:
        return math.floor(self.span_unnorm / self.discrete_step_size) + 1

    def to_dict(self) -> dict:
        """

type(dict)
:return:
"""
        return {
            "decimal_granularity": self._decimal_granularity,
            "min_value": self._min_value,
            "max_value": self._max_value,
        }

    def normalise(self, value):
        return (self.min_unnorm + value + 1) / (self.max_unnorm + 1)

    def denormalise(self, value):
        return (value * self.max_unnorm) - self.min_unnorm

    def clip(self, value):
        return numpy.clip(value, self._min_value, self._max_value)

    def round(self, value):
        return numpy.round(value, self.decimal_granularity)

    def clip_normalise_round(self, value):
        return self.round(self.normalise(self.clip(value)))

    def __repr__(self) -> str:
        return (
            f"<Range>\n"
            f"<decimal_granularity>{self.decimal_granularity}</decimal_granularity>\n"
            f"<min>{self.min}</min>\n"
            f"<max>{self.max}</max>\n"
            f"<normalised>{self.normalised}</normalised>\n"
            f"</Range>\n"
        )

    def __str__(self) -> str:
        return self.__repr__()

    def __unicode__(self) -> str:
        return self.__repr__()

    def sample(self) -> float:
        if self.decimal_granularity == 0:
            return self.cheapest_sample()

        return self.cheaper_sample()
        # return self.expensive_sample()

    def cheapest_sample(self) -> float:
        val = numpy.random.randint(self.min, self.max + 1)

        if isinstance(val, numpy.ndarray):
            return val.item()

        return val

    def cheaper_sample(self) -> float:
        val = numpy.round(numpy.random.random() * self.span, self.decimal_granularity)

        if isinstance(val, numpy.ndarray):
            return val.item()

        return val

    def expensive_sample(self) -> float:
        val = numpy.random.choice(
            numpy.linspace(self.min, self.max, num=self.discrete_steps)
        )

        if isinstance(val, numpy.ndarray):
            return val.item()

        return val


if __name__ == "__main__":
    r = Range(min_value=0, max_value=5, decimal_granularity=2)
    print(r, r.sample())

    r = Range(min_value=0, max_value=2, decimal_granularity=0, normalised=False)
    print(r.span, r.sample(), r.discrete_steps, r.max, r.min)

    a = 2
    assert a == r.denormalise(r.normalise(a))
