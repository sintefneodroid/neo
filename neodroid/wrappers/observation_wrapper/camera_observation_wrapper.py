#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.wrappers import SingleEnvironment
from neodroid.exceptions.exceptions import SensorNotAvailableException
from neodroid.interfaces.neodroid_standard_modules.neodroid_camera_extraction import (
  extract_camera_observation,
  extract_neodroid_camera,
  )


__author__ = 'cnheider'


class CameraObservationWrapper(SingleEnvironment):

  def __init__(self, auto_reset=True, **kwargs):
    super().__init__(**kwargs)
    self._auto_reset = auto_reset

    self.reset()

  def __next__(self):
    if not self._is_connected_to_server:
      return
    return self.fetch_new_frame(None)

  def sensor(self, key):
    if self._last_message:
      state_env_0 = list(self._last_message.values())[0]
      return extract_camera_observation(state_env_0, key)
    raise SensorNotAvailableException

  def update(self):
    return super().react()

  def fetch_new_frame(self, *args, **kwargs):
    message = super().react(*args, **kwargs)
    if message.terminated and self._auto_reset:
      super().reset()
      message = self.fetch_new_frame()

    if message:
      return extract_neodroid_camera(message)
    return None
