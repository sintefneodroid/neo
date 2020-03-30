#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools
from typing import List, Sequence, Tuple

import numpy

from neodroid.utilities.spaces.range import Range

__author__ = "Christian Heider Nielsen"

__all__ = ["Space"]

from warg import cached_property


class Space(object):
    """

"""

    def __init__(self, ranges: Sequence[Range], names: Sequence[str] = ()):
        """

:param ranges:
:param names:
"""
        assert isinstance(ranges, Sequence)
        self._ranges = ranges
        self._names = names

    def project(self, a: Sequence[float]) -> Sequence[float]:
        """

@param a:
@return:
"""
        if self.is_discrete:
            return a
        return a
        # return (a - self.min) / self.span

    def reproject(self, a: Sequence[float]) -> Sequence[float]:
        """

@param a:
@return:
"""
        if self.is_discrete:
            return a
        return a
        # return (a * self.span) + self.min

    def clip(self, values: Sequence) -> numpy.ndarray:
        """

@param values:
@return:
"""
        assert len(self.ranges) == len(values)
        return numpy.array([a.clip(v) for a, v in zip(self._ranges, values)])

    def sample(self) -> Sequence[float]:
        """

@return:
"""
        return [r.sample() for r in self._ranges]

    @property
    def max(self) -> numpy.ndarray:
        """

@return:
"""
        return self.high

    @property
    def min(self) -> numpy.ndarray:
        """

@return:
"""
        return self.low

    @cached_property
    def ranges(self) -> Sequence[Range]:
        """

@return:
"""
        return self._ranges

    @cached_property
    def low(self) -> numpy.ndarray:
        """

@return:
"""
        return numpy.array([motion_space.min_unnorm for motion_space in self._ranges])

    @cached_property
    def high(self) -> numpy.ndarray:
        """

@return:
"""
        return numpy.array([motion_space.max_unnorm for motion_space in self._ranges])

    @cached_property
    def span(self) -> numpy.ndarray:
        """

@return:
"""
        res = self.high - self.low
        assert (res > 0).all()
        return res

    @cached_property
    def decimal_granularity(self) -> List[int]:
        """

@return:
"""
        return [motion_space.decimal_granularity for motion_space in self._ranges]

    @cached_property
    def is_singular(self) -> bool:
        """

@return:
"""
        return len(self._ranges) == 1

    @cached_property
    def is_discrete(self) -> bool:
        """

@return:
"""
        return numpy.array([a.decimal_granularity == 0 for a in self._ranges]).all()

    @cached_property
    def is_mixed(self) -> bool:
        """

@return:
"""
        return (
            numpy.array([a.decimal_granularity != 0 for a in self._ranges]).any()
            and not self.is_continuous
        )

    @cached_property
    def is_continuous(self) -> bool:
        """

@return:
"""
        return numpy.array([a.decimal_granularity != 0 for a in self._ranges]).all()

    @cached_property
    def shape(self) -> Tuple[int, ...]:
        """

@return:
"""
        if self.is_discrete:
            return self.discrete_steps_shape

        return self.continuous_shape

    @cached_property
    def discrete_steps(self) -> int:
        """

@return:
"""
        return sum(self.discrete_steps_shape)

    @cached_property
    def discrete_steps_shape(self) -> Tuple[int, ...]:
        """

@return:
"""
        return (*[r.discrete_steps for r in self._ranges],)

    @cached_property
    def continuous_shape(self) -> Tuple[int, ...]:
        """

@return:
"""
        return (len(self._ranges),)

    @cached_property
    def is_01normalised(self) -> numpy.ndarray:
        """

@return:
"""
        return numpy.array(
            [a.normalised for a in self._ranges if hasattr(a, "normalised")]
        ).all()

    @functools.lru_cache()
    def __repr__(self) -> str:
        """

@return:
"""
        names_str = "".join([str(r.__repr__()) for r in self._names])
        ranges_str = "".join([str(r.__repr__()) for r in self._ranges])

        return (
            f"<Space>\n"
            f"<Names>\n{names_str}</Names>\n"
            f"<Ranges>\n{ranges_str}</Ranges>\n"
            f"</Space>\n"
        )

    @cached_property
    def n(self) -> int:
        """

@return:
"""
        return len(self._ranges)

    @functools.lru_cache()
    def __len__(self) -> int:
        """

@return:
"""
        return self.n


if __name__ == "__main__":
    acs = Space([Range()], ["a"])
    print(acs, acs.decimal_granularity, acs.shape, acs.span)
