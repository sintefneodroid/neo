#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools

from neodroid.messaging.fbs.fbs_state_utilties import deserialise_actuators

__author__ = "Christian Heider Nielsen"

from warg import cached_property


class Actor(object):
    """

    """

    def __init__(self, flat_actor):
        self._flat_actor = flat_actor

    @cached_property
    def actor_name(self):
        """

        @return:
        @rtype:
        """
        return self._flat_actor.ActorName().decode()

    @cached_property
    def is_alive(self):
        """

        @return:
        @rtype:
        """
        return self._flat_actor.Alive()

    def actuator(self, key):
        """

        @param key:
        @type key:
        @return:
        @rtype:
        """
        if key in deserialise_actuators(self._flat_actor):
            return deserialise_actuators(self._flat_actor)[key]

    @cached_property
    def actuators(self):
        """

        @return:
        @rtype:
        """
        return deserialise_actuators(self._flat_actor)

    @functools.lru_cache()
    def __repr__(self):
        actuators = "".join(
            [str(actuators.__repr__()) for actuators in self.actuators.values()]
        )

        return (
            f"<Actor>\n"
            f"<name>{self.actor_name}</name>\n"
            f"<alive>{self.is_alive}</alive>\n"
            f"<Actuators>\n{actuators}</Actuators>\n"
            f"</Actor>\n"
        )

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()
