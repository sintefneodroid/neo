#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from neodroid.utilities.spaces.range import Range
from neodroid.utilities.spaces.space import Space

__author__ = "Christian Heider Nielsen"

__all__ = ["ObservationSpace"]


class ObservationSpace(Space):
    @property
    def space(self) -> Sequence:
        """

        @return:
        @rtype:
        """
        return self.continuous_shape


if __name__ == "__main__":
    acs = ObservationSpace([Range()], ())
    print(acs)
