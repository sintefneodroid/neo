#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools

from neodroid.messaging.fbs.fbs_state_utilties import deserialise_rang

__author__ = "Christian Heider Nielsen"

from neodroid.utilities.spaces.range import Range
from warg import cached_property


class Actuator(object):
    """

    """

    def __init__(self, actuator_name, motion_space):
        self._actuator_name = actuator_name
        self._range = motion_space

    @cached_property
    def actuator_name(self):
        """

        @return:
        @rtype:
        """
        return self._actuator_name

    @cached_property
    def motion_space(self) -> Range:
        """

        @return:
        @rtype:
        """
        return deserialise_rang(self._range)

    @functools.lru_cache()
    def __repr__(self):
        return (
            f"<Actuator>\n"
            f"<name>{self.actuator_name}</name>\n"
            f"<motion_space>{self.motion_space}</motion_space>\n"
            f"</Actuator>\n"
        )

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()
