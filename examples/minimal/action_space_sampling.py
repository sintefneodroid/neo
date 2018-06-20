#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

__author__ = 'cnheider'

import neodroid.wrappers.formal_wrapper as neo


def main():
  _environments = neo.make(environment_name='obs', connect_to_running=False)
  _environments.reset()

  i=0
  freq=100
  time_s = time.time()
  while _environments.is_connected:
    actions = _environments.action_space.sample()
    observations, rewards, terminated, info = _environments.act(input_reaction=actions)

    time_now = time.time()
    if i % freq == 0:
      fps = (1 / (time_now - time_s))
      print(f'fps:[{fps}]')

    i += 1
    time_s = time_now

    if terminated:
      _environments.reset()


if __name__ == '__main__':
  main()
