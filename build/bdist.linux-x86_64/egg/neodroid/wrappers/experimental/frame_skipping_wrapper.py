#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

import logging

import gym

_logger = logging.getLogger(__name__)


class FrameSkippingWrapper(gym.Wrapper):

  def __init__(self, env, skips):
    super().__init__(env)
    self._skips = skips

  def _step(self, action):

    state_buffer = []
    reward_buffer = []
    info_buffer = []
    terminated = False

    for _ in range(self._skips):

      observation, signal, terminated, info = self.env.act(action[0, 0])
      next_state = self.env.get_screen()
      state_buffer.append(next_state)
      reward_buffer.append(signal)
      info_buffer.append(info)

      if terminated:
        break

    return state_buffer, reward_buffer, terminated, info_buffer

  def _reset(self):
    return self.env.reset()
