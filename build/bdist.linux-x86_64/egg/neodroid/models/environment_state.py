#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cnheider'

import neodroid.messaging


# @pretty_print
class EnvironmentState(object):

  def __init__(self, fbs_state):
    super().__init__()
    self._fbs_state = fbs_state

  @property
  def environment_name(self):
    return self._fbs_state.EnvironmentName()

  @property
  def signal(self):
    return self._fbs_state.Signal()

  @property
  def observables(self):
    return neodroid.messaging.deserialise_observables(self._fbs_state)

  @property
  def unobservables(self):
    return neodroid.messaging.deserialise_unobservables(self._fbs_state)

  @property
  def frame_number(self):
    return self._fbs_state.FrameNumber()

  @property
  def terminated(self):
    return self._fbs_state.Terminated()

  @property
  def termination_reason(self):
    return self._fbs_state.TerminationReason().decode()

  @property
  def debug_message(self):
    return self._fbs_state.DebugMessage().decode()

  @property
  def total_energy_spent(self):
    return self._fbs_state.TotalEnergySpent()

  @property
  def description(self):
    if self._fbs_state.EnvironmentDescription():
      return neodroid.messaging.deserialise_description(
          self._fbs_state.EnvironmentDescription()
          )

  @property
  def sensors(self):
    return self.observers

  @property
  def observers(self):
    return neodroid.messaging.deserialise_observers(self._fbs_state)

  def observer(self, key):
    if key in neodroid.messaging.deserialise_observers(self._fbs_state):
      return neodroid.messaging.deserialise_observers(self._fbs_state)[key]

  def sensor(self, key):
    return self.observer(key)

  def to_gym(self):
    return (self.observers, self.signal, self.terminated, self)

  def __repr__(self):
    observers_str = ''.join(
        [str(observer.__repr__()) for observer in self.observers.values()]
        )

    description_str = str(self.description)
    return (f'<EnvironmentState>\n'
            f'<total_energy_spent>{self.total_energy_spent}</total_energy_spent>\n'
            f'<frame_number>{self.frame_number}</frame_number>\n'
            f'<reward>{self.signal}</reward>\n'
            f'<terminated>{self.terminated}</terminated>\n'
            f'<Observers>\n{observers_str}</Observers>\n'
            f'{self.description}\n'
            f'{self.unobservables}\n'
            f'</EnvironmentState>\n')

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()

  def __iter__(self):
    return self.observables

  '''
  def __len__(self):
    return len(self.observables)
  '''
