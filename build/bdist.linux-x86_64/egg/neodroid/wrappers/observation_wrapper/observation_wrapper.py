#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from warnings import warn

from neodroid.utilities.messaging_utilities.neodroid_camera_extraction import (
  extract_camera_observation,
  extract_neodroid_camera,
  )
from neodroid.wrappers.experimental.single_environment_wrapper import SingleEnvironmentWrapper

__author__ = 'cnheider'

from neodroid.utilities import flattened_observation


class ObservationWrapper(SingleEnvironmentWrapper):

  def __next__(self):
    if not self._is_connected_to_server:
      return
    return self.fetch_new_frame(None)

  def randomise(self, input_reaction, **kwargs):
    return self.fetch_new_frame(input_reaction, **kwargs)

  def observer(self, key):
    if self._last_message:
      return self._sensor(key)
    warn('No message available')
    return None

  def configure(self, *args, **kwargs):
    message = super().reset(*args, **kwargs)
    if message:
      return flattened_observation(message), message
    return None, None

  def fetch_new_frame(self, *args, **kwargs):
    message = super().observe(*args, **kwargs)
    if message:
      return (
        flattened_observation(message),
        message.signal,
        message.terminated,
        message,
        )
    return None, None, None, None

  def quit(self, *args, **kwargs):
    return self.close(*args, **kwargs)


class SensorNotAvailableException(Exception):
  def __init__(self):
    super().__init__()


class CameraObservationWrapper(SingleEnvironmentWrapper):

  def __init__(self, auto_reset=True, image_size=(None, None, 4), **kwargs):
    super().__init__(**kwargs)
    self._auto_reset = auto_reset
    self._image_size = image_size
    self.reset()

  def __next__(self):
    if not self._is_connected_to_server:
      return
    return self.fetch_new_frame(None)

  def sensor(self, key):
    if self._last_message:
      state_env_0 = list(self._last_message.values())[0]
      return extract_camera_observation(state_env_0, key, image_size=self._image_size)
    raise SensorNotAvailableException

  def update(self):
    return super().react()

  def fetch_new_frame(self, *args, **kwargs):
    message = super().react(*args, **kwargs)
    if message.terminated and self._auto_reset:
      super().reset()
      message = self.fetch_new_frame()

    if message:
      return extract_neodroid_camera(message, image_size=self._image_size)
    return None
