#!/usr/bin/env python3
# coding=utf-8
__author__ = 'cnheider'


class Configuration(object):

  def __init__(self, configurable_name, configurable_value):
    self._configurable_name = configurable_name
    self._configurable_value = configurable_value

  @property
  def configurable_name(self):
    return self._configurable_name

  @property
  def configurable_value(self):
    return self._configurable_value

  def to_dict(self):
    return {
      '_configurable_name': self._configurable_name,
      '_configurable_value':self._configurable_value,
      }

  def __repr__(self):
    return '<Configuration>\n' + '  <configurable_name>' + str(
        self._configurable_name
        ) + '</configurable_name>\n' + '  <configurable_value>' + str(
        self._configurable_value
        ) + '</configurable_value>\n' + '</Configuration>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
