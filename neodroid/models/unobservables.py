#!/usr/bin/env python3
# coding=utf-8
__author__ = 'cnheider'

import numpy as np

import neodroid.messaging


class Unobservables(object):
  def __init__(self, unobservables):
    self._unobservables = unobservables

  @property
  def unobservables(self):
    return self._unobservables

  @property
  def poses_numpy(self):
    return neodroid.messaging.create_poses(self._unobservables)

  @property
  def bodies_numpy(self):
    return neodroid.messaging.create_bodies(self._unobservables)

  @property
  def state_configuration(self):
    return np.array([self.poses_numpy().flatten(), self.bodies_numpy().flatten()]).flatten()

  def __repr__(self):
    return '<Unobservables>\n' + \
           '  <Poses>\n' + \
           str(self.poses_numpy) + \
           '  </Poses>\n' + \
           '  <Bodies>\n' + \
           str(self.bodies_numpy) + \
           '  </Bodies>\n' + \
           '</Unobservables>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
