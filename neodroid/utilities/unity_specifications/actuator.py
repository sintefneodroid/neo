#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.messaging.fbs.fbs_state_utilties import deserialise_space

__author__ = 'Christian Heider Nielsen'


class Actuator(object):

  def __init__(self, actuator_name, motion_space):
    self._actuator_name = actuator_name
    self._motion_space = motion_space

  @property
  def actuator_name(self):
    return self._actuator_name

  @property
  def motion_space(self):
    return deserialise_space(self._motion_space)

  def __repr__(self):
    return (f'<Actuator>\n'
            f'<name>{self.actuator_name}</name>\n'
            f'<motion_space>{self.motion_space}</motion_space>\n'
            f'</Actuator>\n')

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
