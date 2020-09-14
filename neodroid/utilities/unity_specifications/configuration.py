#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"

import functools

from warg import cached_property


class Configuration(object):
    """

  """

    def __init__(self, configurable_name, configurable_value):
        self._configurable_name = configurable_name
        self._configurable_value = configurable_value

    @cached_property
    def configurable_name(self):
        """

    @return:
    @rtype:
    """
        return self._configurable_name

    @cached_property
    def configurable_value(self):
        """

    @return:
    @rtype:
    """
        return self._configurable_value

    @functools.lru_cache()
    def to_dict(self):
        """

    @return:
    @rtype:
    """
        return {
            "_configurable_name": self._configurable_name,
            "_configurable_value": self._configurable_value,
        }

    @functools.lru_cache()
    def __repr__(self):
        return (
            f"<Configuration>\n"
            f"<configurable_name>{self._configurable_name}</configurable_name>\n"
            f"<configurable_value>{self._configurable_value}>/configurable_value>\n"
            f"</Configuration>\n"
        )

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()
