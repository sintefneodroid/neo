#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from neodroid.utilities.spaces.space import Space

from neodroid.utilities.spaces.range import Range

__author__ = "Christian Heider Nielsen"

__all__ = ["ObservationSpace"]


class ObservationSpace(Space):
    @property
    def space(self) -> Sequence:
        return self.continuous_shape


if __name__ == "__main__":
    acs = ObservationSpace([Range()], ())
    print(acs)
