#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Mapping

import numpy
from attr import dataclass

__author__ = "Christian Heider Nielsen"

from neodroid.utilities import NoEnvironment
from neodroid.utilities.unity_specifications import EnvironmentSnapshot
from warg.mixins import IterDictValuesMixin, OrdinalIndexingDictMixin

__all__ = ["VectorPoints", "NumpyVectorPoints", "VectorEnvironmentSnapshot"]


@dataclass
class VectorPoints(IterDictValuesMixin, OrdinalIndexingDictMixin):
    __slots__ = ["observables", "signal", "terminated"]
    observables: List[List[float]]
    signal: List[float]
    terminated: List[bool]

    def __len__(self):
        """

@return:
"""
        return len(self.terminated)


@dataclass
class NumpyVectorPoints(IterDictValuesMixin, OrdinalIndexingDictMixin):
    __slots__ = ["observables", "signal", "terminated"]
    observables: numpy.ndarray
    signal: numpy.ndarray
    terminated: numpy.ndarray

    def __len__(self):
        """

@return:
"""
        return len(self.terminated)


class VectorEnvironmentSnapshot(object):
    def __init__(self, environment_snapshots: Mapping[str, EnvironmentSnapshot]):
        keys = environment_snapshots.keys()
        if not len(keys):
            raise NoEnvironment
        self._environment_name = next(iter(keys))
        self._environment_snapshots = environment_snapshots

        o, s, t = zip(
            *[
                (e_.observables, e_.signal, e_.terminated)
                for e_ in environment_snapshots.values()
            ]
        )

        os = numpy.stack(o)
        ss = numpy.stack(s)[:, numpy.newaxis]
        ts = numpy.stack(t)[:, numpy.newaxis]

        self._vector_points = NumpyVectorPoints(os, ss, ts)

    @property
    def environment_name(self) -> str:
        return self._environment_name

    @property
    def observables(self) -> numpy.ndarray:
        return self._vector_points.observables

    @property
    def signal(self) -> numpy.ndarray:
        return self._vector_points.signal

    @property
    def terminated(self) -> numpy.ndarray:
        return self._vector_points.terminated

    @property
    def as_tuple(self):
        return tuple(*self._vector_points)

    @property
    def vector_points(self) -> NumpyVectorPoints:
        return self._vector_points

    def __repr__(self):
        return (
            f"<VectorEnvironmentSnapshot>\n"
            f"<observables>{self.observables}</observables>\n"
            f"<signal>{self.signal}</signal>\n"
            f"<terminated>{self.terminated}</terminated>\n"
            f"</VectorEnvironmentSnapshot>\n"
        )

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()


if __name__ == "__main__":
    pass
