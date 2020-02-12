#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from neodroid.messaging.fbs.fbs_state_utilties import deserialise_space

__author__ = "Christian Heider Nielsen"

from neodroid.utilities.spaces.range import Range


class Sensor(object):
    r"""

  """

    def __init__(self, sensor_name, sensor_range, sensor_value, is_image):
        self._range = sensor_range
        self._sensor_name = sensor_name
        self._value = sensor_value
        self._is_image = is_image

    @property
    def name(self):
        return self._sensor_name

    @property
    def is_image(self):
        return self._is_image

    @property
    def space(self) -> List[Range]:
        return self._range

    @property
    def value(self):
        return self._value

    def __repr__(self):
        return (
            f"<Observer>\n"
            f"<observation_name>{self._sensor_name}</observation_name>\n"
            f"<observation_space>{self.space}</observation_space>\n"
            f"<observation_value>{self.value}</observation_value>\n"
            f"</Observer>\n"
        )

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)

    def __call__(self, *args, **kwargs):
        return self.value

    def __cmp__(self, other):
        return self.value == other

    def __next__(self):
        return self.value
