#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from warnings import warn

from neodroid.wrappers.single_environment_wrapper import SingleEnvironmentWrapper

__author__ = 'cnheider'

import numpy as np

from neodroid.utilities import flattened_observation


class NeodroidGymWrapper(SingleEnvironmentWrapper):

  def step(self, action=None, *args, **kwargs):
    # action = action.flatten()
    message = super().react(input_reaction=action, **kwargs)
    if message:
      return (
        np.array(flattened_observation(message)),
        message.signal,
        message.terminated,
        message,
        )
    return None, None, None, None

  def reset(self, *args, **kwargs):
    message = super().reset(*args, **kwargs)
    if message:
      return np.array(flattened_observation(message))
    return None

  def render(self, *args, **kwargs):
    pass

  def sensor(self, key):
    if self._last_message:
      return self._observer(key)
    warn('No message available')
    return None

  def __next__(self):
    if not self._is_connected_to_server:
      return
    return self.react()
