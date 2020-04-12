#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools

from neodroid.messaging.fbs.fbs_state_utilties import (
    deserialise_bodies,
    deserialise_poses,
)

__author__ = "Christian Heider Nielsen"

import numpy

from warg import cached_property


class Unobservables(object):
    """

    """

    def __init__(self, unobservables):
        self._unobservables = unobservables

    @property
    def unobservables(self):
        """

        @return:
        @rtype:
        """
        return self._unobservables

    @cached_property
    def poses_numpy(self):
        """

        @return:
        @rtype:
        """
        if self._unobservables:
            return deserialise_poses(self._unobservables)

    @cached_property
    def bodies_numpy(self):
        """

        @return:
        @rtype:
        """
        if self._unobservables:
            return deserialise_bodies(self._unobservables)

    @cached_property
    def state_configuration(self):
        """

        @return:
        @rtype:
        """
        return numpy.array(
            [self.poses_numpy.flatten(), self.bodies_numpy.flatten()]
        ).flatten()

    @functools.lru_cache()
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
