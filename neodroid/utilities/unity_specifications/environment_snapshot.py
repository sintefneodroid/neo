#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Callable, Sequence, Iterable

from neodroid.messaging.fbs.FBSModels.FState import FState
from neodroid.messaging.fbs.fbs_state_utilties import (deserialise_description,
                                                       deserialise_observables,
                                                       deserialise_unobservables,
                                                       )

__author__ = 'Christian Heider Nielsen'


class EnvironmentSnapshot(object):

  def __init__(self, fbs_state: FState = None):

    self._fbs_state = fbs_state

  def _environment_name(self):
    return self._fbs_state.EnvironmentName()

  @property
  def environment_name(self):
    if not isinstance(self._environment_name, Callable):
      return self._environment_name
    return self._environment_name()

  def _signal(self) -> float:
    return self._fbs_state.Signal()

  @property
  def signal(self) -> float:
    if not isinstance(self._signal, Callable):
      return self._signal
    return self._signal()

  def _observables(self) -> Iterable:
    return deserialise_observables(self._fbs_state)

  @property
  def observables(self) -> Iterable:
    if not isinstance(self._observables, Callable):
      return self._observables
    return self._observables()

  def _unobservables(self):
    return deserialise_unobservables(self._fbs_state)

  @property
  def unobservables(self):
    if not isinstance(self._unobservables, Callable):
      return self._unobservables
    return self._unobservables()

  def _frame_number(self):
    return self._fbs_state.FrameNumber()

  @property
  def frame_number(self):
    if not isinstance(self._frame_number, Callable):
      return self._frame_number
    return self._frame_number()

  def _terminated(self):
    return self._fbs_state.Terminated()

  @property
  def terminated(self):
    if not isinstance(self._terminated, Callable):
      return self._terminated
    return self._terminated()

  def _termination_reason(self):
    return self._fbs_state.TerminationReason().decode()

  @property
  def termination_reason(self):
    if not isinstance(self._termination_reason, Callable):
      return self._termination_reason
    return self._termination_reason()

  def _extra_serialised_message(self):
    return self._fbs_state.ExtraSerialisedMessage().decode()

  @property
  def extra_serialised_message(self):
    if not isinstance(self._extra_serialised_message, Callable):
      return self._extra_serialised_message
    return self._extra_serialised_message()

  @property
  def description(self):
    if self._fbs_state.EnvironmentDescription():
      return deserialise_description(self._fbs_state.EnvironmentDescription())

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

  @staticmethod
  def from_gym_like_out(observables,
                        signal,
                        terminated,
                        info):
    snapshot = EnvironmentSnapshot(None)
    snapshot._observables = observables
    snapshot._signal = signal
    snapshot._terminated = terminated
    snapshot._extra_serialised_message = info
    return snapshot

  def to_dict(self):
    # inspect.getmembers(a)
    return dict(vars(self))

  def to_json(self):
    import json
    encoder = json.JSONEncoder()
    return encoder.encode(self.to_dict())

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


if __name__ == '__main__':
  es = EnvironmentSnapshot.from_gym_like_out([0, 2, 1], 0, terminated=False, info=None)
  print(es.to_json())
