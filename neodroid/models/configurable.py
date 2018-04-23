#!/usr/bin/env python3
# coding=utf-8
__author__ = 'cnheider'


# @pretty_print
class Configurable(object):
  def __init__(self, configurable_name, observation):
    self._configurable_name = configurable_name
    self._observation = observation

  @property
  def configurable_name(self):
    return self._configurable_name

  @property
  def observation(self):
    return self._observation

  def to_dict(self):
    return {
      '_configurable_name':  self._configurable_name,
      '_configurable_value': self._valid_range
      }

  def __repr__(self):
    return '<Configurable>\n' + \
           '  <configurable_name>' + str(self._configurable_name) + \
           '</configurable_name>\n' + \
           '  <observation>\n' + str(self._observation) + \
           '</observation>\n' + \
           '</Configurable>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
