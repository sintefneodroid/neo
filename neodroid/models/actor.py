#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

import neodroid.messaging


class Actor(object):

  def __init__(self, flat_actor):
    self._flat_actor = flat_actor

  @property
  def actor_name(self):
    return self._flat_actor.ActorName()

  @property
  def is_alive(self):
    return self._flat_actor.Alive()

  def motor(self, key):
    if key in neodroid.messaging.deserialise_motors(self._flat_actor):
      return neodroid.messaging.deserialise_motors(self._flat_actor)[key]

  @property
  def motors(self):
    return neodroid.messaging.deserialise_motors(self._flat_actor)

  def __repr__(self):
    motors_str = ''.join([str(motor.__repr__()) for motor in self.motors.values()])

    return (f'<Actor>\n'
            f'<name>{self.actor_name.decode("utf-8")}</name>\n'
            f'<alive>{self.is_alive}</alive>\n'
            f'<Motors>\n{motors_str}</Motors>\n'
            f'</Actor>\n')

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
