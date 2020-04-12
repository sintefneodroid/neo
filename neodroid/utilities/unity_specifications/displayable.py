#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"

# @pretty_print
from warg import cached_property


class Displayable(object):
    """

    """

    def __init__(self, displayable_name, displayable_value):
        self._displayable_name = displayable_name
        self._displayable_value = displayable_value

    @cached_property
    def displayable_name(self):
        """

        @return:
        @rtype:
        """
        return self._displayable_name

    @cached_property
    def displayable_value(self):
        """

        @return:
        @rtype:
        """
        return self._displayable_value

    def to_dict(self):
        """

        @return:
        @rtype:
        """
        return {
            "_displayable_name": self._displayable_name,
            "_displayable_value": self._displayable_value,
        }

    def __repr__(self):
        return (
            f"<Displayable>\n"
            f"<displayable_name>{self._displayable_name}</displayable_name>\n"
            f"<displayable_value>\n{self._displayable_value}</displayable_value>\n"
            f"</Displayable>\n"
        )

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()
