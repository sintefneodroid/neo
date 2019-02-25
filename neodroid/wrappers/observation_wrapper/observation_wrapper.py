#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from warnings import warn

import torch

from neodroid.neodroid_utilities.messaging_utilities.neodroid_camera_extraction import (
  extract_neodroid_camera,
  extract_camera_observation,
  )
from neodroid.wrappers.utility_wrappers.single_environment_wrapper import SingleEnvironmentWrapper

__author__ = 'cnheider'

from neodroid.neodroid_utilities import flattened_observation
import numpy as np

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
    super().observe()

  def fetch_new_frame(self, *args, **kwargs):
    message = super().observe(*args, **kwargs)
    if message:
      return extract_neodroid_camera(message)
    return None

def channel_transform(inp):
  inp = inp / 255.0
  inp = np.clip(inp, 0, 1)
  inp = inp.transpose((2, 0, 1))
  return inp

def neodroid_batch_data_iterator(env, device, batch_size = 12):
  while True:
    predictors = []
    responses = []
    while len(predictors) < batch_size:
      env.update()
      rgb_arr = env.sensor('RGBCameraObserver')
      seg_arr = env.sensor('LayerSegmentationCameraObserver')

      red_mask = np.zeros(seg_arr.shape[:-1])
      green_mask = np.zeros(seg_arr.shape[:-1])
      blue_mask = np.zeros(seg_arr.shape[:-1])

      reddish = seg_arr[:, :, 0] > 50
      greenish = seg_arr[:, :, 1] > 50
      blueish = seg_arr[:, :, 2] > 50

      red_mask[reddish] = 1
      green_mask[greenish] = 1
      blue_mask[blueish] = 1

      predictors.append(channel_transform(rgb_arr))
      responses.append(np.asarray([red_mask, blue_mask, green_mask]))
    yield torch.FloatTensor(predictors).to(device), torch.FloatTensor(responses).to(device)
