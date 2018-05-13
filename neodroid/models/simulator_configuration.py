#!/usr/bin/env python3
# coding=utf-8
__author__ = 'cnheider'

class SimulatorConfiguration(object):

  def __init__(self, fbs_configuration, api_version):
    self._fbs_configuration = fbs_configuration
    self._api_version = api_version

  @property
  def simulator_configuration(self):
    return self._fbs_configuration


  @property
  def api_version(self):
    return self._api_version.decode()