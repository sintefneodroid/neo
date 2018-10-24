#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from warnings import warn

from neodroid.wrappers.single_environment_wrapper import SingleEnvironmentWrapper

__author__ = 'cnheider'

from neodroid.neodroid_utilities import flattened_observation


class ObservationWrapper(SingleEnvironmentWrapper):

  def __next__(self):
    if not self._is_connected_to_server:
      return
    return self.get_frame(None)

  def randomise(self, input_reaction, **kwargs):
    return self.get_frame(input_reaction, **kwargs)

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

  def get_frame(self, *args, **kwargs):
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
