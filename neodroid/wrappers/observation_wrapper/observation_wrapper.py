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
      return self._observer(key)
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


class CameraObservationWrapper(SingleEnvironmentWrapper):

  def __next__(self):
    if not self._is_connected_to_server:
      return
    return self.fetch_new_frame(None)

  def sensor(self, key):
    if self._last_message:
      state_env_0 = list(self._last_message.values())[0]
      return extract_camera_observation(state_env_0, key)
    warn('No new message received')
    return None

  def update(self):
    return super().observe()

  def fetch_new_frame(self, *args, **kwargs):
    message = super().observe(*args, **kwargs)
    if message:
      return extract_neodroid_camera(message)
    return None

