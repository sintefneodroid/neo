#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"

from typing import Any, Dict


class Motion(object):
    """

  """

    def __init__(self, actor_name: str, actuator_name: str, strength: float):
        """

:param actor_name:
:param actuator_name:
:param strength: Strength has a possible direction given by the sign of the float
"""
        self._actor_name = actor_name
        self._actuator_name = actuator_name
        self._strength = strength

    @property
    def actor_name(self) -> str:
        """

    @return:
    @rtype:
    """
        return self._actor_name

    @property
    def actuator_name(self) -> str:
        """

    @return:
    @rtype:
    """
        return self._actuator_name

    @property
    def strength(self) -> float:
        """

    @return:
    @rtype:
    """
        return self._strength

    def to_dict(self) -> Dict[str, Any]:
        """

    @return:
    @rtype:
    """
        return {
            "_actor_name": self._actor_name,
            "_motor_name": self._actuator_name,
            "_strength": self._strength,
        }

    def __repr__(self) -> str:
        return (
            f"<Motion>\n"
            f"<actor_name>{self._actor_name}</actor_name>\n"
            f"<motor_name>{self._actuator_name}</motor_name>\n"
            f"<strength>{self._strength}</strength>\n"
            f"</Motion>\n"
        )

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()
