#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

import neodroid.messaging


class Actor(object):

  def __init__(self, flat_actor):
    self._flat_actor = flat_actor

  @property
  def actor_name(self):
    return self._flat_actor.ActorName().decode()

  @property
  def is_alive(self):
    return self._flat_actor.Alive()

  def actuator(self, key):
    if key in neodroid.messaging.deserialise_actuators(self._flat_actor):
      return neodroid.messaging.deserialise_actuators(self._flat_actor)[key]

  @property
  def actuators(self):
    return neodroid.messaging.deserialise_actuators(self._flat_actor)

  def __repr__(self):
    actuators = ''.join([str(actuators.__repr__()) for actuators in self.actuators.values()])

    return (f'<Actor>\n'
            f'<name>{self.actor_name}</name>\n'
            f'<alive>{self.is_alive}</alive>\n'
            f'<Actuators>\n{actuators}</Actuators>\n'
            f'</Actor>\n')

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
