#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

import neodroid.messaging


class Motor(object):

  def __init__(self, motor_name, motion_space, energy_spent):
    self._motor_name = motor_name
    self._motion_space = motion_space
    self._energy_spent = energy_spent

  @property
  def motor_name(self):
    return self._motor_name

  @property
  def motion_space(self):
    return neodroid.messaging.deserialise_space(self._motion_space)

  @property
  def energy_spent(self):
    return self._energy_spent

  def __repr__(self):
    return (f'<Motor>\n'
            f'<name>{self.motor_name}</name>\n'
            f'<motion_space>{self.motion_space}</motion_space>\n'
            f'<energy_spent>{self.energy_spent}</energy_spent>\n'
            f'</Motor>\n')

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
