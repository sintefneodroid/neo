#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

import neodroid.messaging


class Actuator(object):

  def __init__(self, actuator_name, motion_space, energy_spent):
    self._actuator_name = actuator_name
    self._motion_space = motion_space
    self._energy_spent = energy_spent

  @property
  def actuator_name(self):
    return self._actuator_name

  @property
  def motion_space(self):
    return neodroid.messaging.deserialise_space(self._motion_space)

  @property
  def energy_spent(self):
    return self._energy_spent

  def __repr__(self):
    return (f'<Actuator>\n'
            f'<name>{self.actuator_name}</name>\n'
            f'<motion_space>{self.motion_space}</motion_space>\n'
            f'<energy_spent>{self.energy_spent}</energy_spent>\n'
            f'</Actuator>\n')

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
