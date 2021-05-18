#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "Christian Heider Nielsen"

# @pretty_print
import functools
from typing import Any, List

from trolls.spaces import Range
from warg import cached_property


class Configurable(object):
    """ """

    def __init__(
        self,
        configurable_name: str,
        configurable_value: Any,
        space: List[Range],  #:List[FRange],
    ):
        self._configurable_name = configurable_name
        self._configurable_value = configurable_value
        self._configurable_space = space

    @cached_property
    def configurable_name(self):
        """

        :return:
        :rtype:
        """
        return self._configurable_name

    @cached_property
    def configurable_value(self):
        """

        :return:
        :rtype:
        """
        return self._configurable_value

    @cached_property
    def configurable_space(self):
        """

        :return:
        :rtype:
        """
        if self._configurable_space:
            # space = deserialise_space(self._configurable_space) #Already done
            space = self._configurable_space
            return space

    @functools.lru_cache()
    def to_dict(self):
        """

        :return:
        :rtype:
        """
        return {
            "configurable_name": self.configurable_name,
            "configurable_value": self.configurable_value,
            "configurable_space": self.configurable_space,
        }

    @functools.lru_cache()
    def __repr__(self):
        return (
            f"<Configurable>\n"
            f"<configurable_name>{self.configurable_name}</configurable_name>\n"
            f"<configurable_value>{self.configurable_value}</configurable_value>\n"
            f"<configurable_space>\n{self.configurable_space}</configurable_space>\n"
            f"</Configurable>\n"
        )

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()
