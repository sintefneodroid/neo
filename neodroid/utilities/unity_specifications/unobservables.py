#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.messaging.fbs.fbs_state_utilties import (
    deserialise_poses,
    deserialise_bodies,
)

__author__ = "Christian Heider Nielsen"

import numpy


class Unobservables(object):
    def __init__(self, unobservables):
        self._unobservables = unobservables

    @property
    def unobservables(self):
        return self._unobservables

    @property
    def poses_numpy(self):
        if self._unobservables:
            return deserialise_poses(self._unobservables)

    @property
    def bodies_numpy(self):
        if self._unobservables:
            return deserialise_bodies(self._unobservables)

    @property
    def state_configuration(self):
        return numpy.array(
            [self.poses_numpy().flatten(), self.bodies_numpy().flatten()]
        ).flatten()

    def __repr__(self):
        return (
            f"<Unobservables>\n"
            f"<Poses>\n{self.poses_numpy}</Poses>\n"
            f"<Bodies>\n{self.bodies_numpy}</Bodies>\n"
            f"</Unobservables>\n"
        )

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()
