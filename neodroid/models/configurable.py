#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import neodroid
import neodroid.messaging

__author__ = 'cnheider'


# @pretty_print
class Configurable(object):

  def __init__(self, configurable_name, configurable_value, space):
    self._configurable_name = configurable_name
    self._configurable_value = configurable_value
    self._configurable_space = space

  @property
  def configurable_name(self):
    return self._configurable_name

  @property
  def configurable_value(self):
    return self._configurable_value

  @property
  def configurable_space(self):
    if self._configurable_space:
      space = neodroid.messaging.deserialise_space(self._configurable_space)
      return space

  def to_dict(self):
    return {
      'configurable_name': self.configurable_name,
      'configurable_value':self.configurable_value,
      'configurable_space':self.configurable_space
      }

  def __repr__(self):
    return (f'<Configurable>\n'
            f'<configurable_name>{self.configurable_name}</configurable_name>\n'
            f'<configurable_value>{self.configurable_value}</configurable_value>\n'
            f'<configurable_space>\n{self.configurable_space}</configurable_space>\n'
            f'</Configurable>\n')

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
