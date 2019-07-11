#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import Callable

__author__ = 'cnheider'

import neodroid.messaging

class EnvironmentSnapshot(object):

  def __init__(self, fbs_state):
    super().__init__()
    self._fbs_state = fbs_state

  @property
  def environment_name(self):
    return self._fbs_state.EnvironmentName()

  def _signal(self):
    return self._fbs_state.Signal()

  @property
  def signal(self):
    if isinstance(self._signal, Callable):
      return self._signal()
    return self._signal

  def _observables(self):
    return neodroid.messaging.deserialise_observables(self._fbs_state)

  @property
  def observables(self):
    if isinstance(self._observables, Callable):
      return self._observables()
    return self._observables

  @property
  def unobservables(self):
    return neodroid.messaging.deserialise_unobservables(self._fbs_state)

  @property
  def frame_number(self):
    return self._fbs_state.FrameNumber()

  def _terminated(self):
    return self._fbs_state.Terminated()

  @property
  def terminated(self):
    if isinstance(self._observables, Callable):
      return self._terminated()
    return self._terminated

  @property
  def termination_reason(self):
    return self._fbs_state.TerminationReason().decode()

  @property
  def debug_message(self):
    return self._fbs_state.DebugMessage().decode()


  @property
  def description(self):
    if self._fbs_state.EnvironmentDescription():
      return neodroid.messaging.deserialise_description(
          self._fbs_state.EnvironmentDescription()
          )

  @property
  def sensors(self):
    return self.description.sensors

  def sensor(self, key):
    return self.description.sensor(key)

  @property
  def configurables(self):
    return self.description.configurables

  def configurable(self, key):
    return self.description.configurable(key)

  def to_gym_like_output(self):
    return self.observables, self.signal, self.terminated, self

  def __repr__(self):
    return (f'<EnvironmentState>\n'
            f'<frame_number>{self.frame_number}</frame_number>\n'
            f'<reward>{self.signal}</reward>\n'
            f'<terminated>{self.terminated}</terminated>\n'
            f'{self.description}\n'
            f'{self.unobservables}\n'
            f'</EnvironmentState>\n')

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
