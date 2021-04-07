#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Generator, Tuple

from neodroid.utilities.spaces import ActionSpace

__author__ = "Christian Heider Nielsen"

__all__ = ["ToIntWrapper"]


class ToIntWrapper:
    """"""

    def __init__(self, action_space: ActionSpace):
        self.action_space = action_space

    def sample(self) -> Generator[int, Any, None]:
        """

        :return:
        :rtype:
        """
        return (round(a) for a in self.action_space.sample())

    def __getattr__(self, item):
        return getattr(self.action_space, item)
