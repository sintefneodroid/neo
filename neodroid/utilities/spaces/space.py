#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence, List, Tuple

import numpy

from neodroid.utilities.spaces.range import Range

__author__ = "Christian Heider Nielsen"

__all__ = ["Space"]


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

    @property
    def ranges(self) -> Sequence[Range]:
        return self._ranges

    def sample(self) -> Sequence[float]:
        return [r.sample() for r in self._ranges]

    @property
    def low(self) -> List:
        return [motion_space.min_unnorm for motion_space in self._ranges]

    @property
    def high(self) -> List:
        return [motion_space.max_unnorm for motion_space in self._ranges]

    @property
    def max(self) -> List:
        return self.high

    @property
    def min(self) -> List:
        return self.low

    @property
    def decimal_granularity(self) -> List:
        return [motion_space.decimal_granularity for motion_space in self._ranges]

    @property
    def is_singular(self) -> bool:
        return len(self._ranges) == 1

    @property
    def is_discrete(self) -> bool:
        return numpy.array([a.decimal_granularity == 0 for a in self._ranges]).all()

    @property
    def is_mixed(self) -> bool:
        return numpy.array([a.decimal_granularity != 0 for a in self._ranges]).any()

    @property
    def is_continuous(self) -> bool:
        return numpy.array([a.decimal_granularity != 0 for a in self._ranges]).all()

    @property
    def shape(self) -> Tuple:
        if self.is_discrete:
            return self.discrete_steps_shape

        return self.continuous_shape

    @property
    def discrete_steps(self) -> int:
        return sum(self.discrete_steps_shape)

    @property
    def discrete_steps_shape(self) -> Tuple[int, ...]:
        return (*[r.discrete_steps for r in self._ranges],)

    @property
    def continuous_shape(self) -> Tuple:
        return (len(self._ranges),)

    @property
    def is_01normalised(self) -> numpy.ndarray:
        return numpy.array(
            [a.normalised for a in self._ranges if hasattr(a, "normalised")]
        ).all()

    def clip(self, values: Sequence) -> numpy.ndarray:
        assert len(self.ranges) == len(values)
        return numpy.array([a.clip(v) for a, v in zip(self._ranges, values)])

    def __repr__(self) -> str:
        names_str = "".join([str(r.__repr__()) for r in self._names])
        ranges_str = "".join([str(r.__repr__()) for r in self._ranges])

        return (
            f"<Space>\n"
            f"<Names>\n{names_str}</Names>\n"
            f"<Ranges>\n{ranges_str}</Ranges>\n"
            f"</Space>\n"
        )

    @property
    def n(self) -> int:
        return len(self._ranges)

    def __len__(self) -> int:
        return self.n


if __name__ == "__main__":
    acs = Space([], [])
    print(acs, acs.decimal_granularity)
