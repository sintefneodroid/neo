#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

__author__ = 'cnheider'

import neodroid as neo


def main():
  _environments = neo.make(connect_to_running=True,verbose=True)
  _environments.reset()

  i = 0
  freq = 100
  time_s = time.time()
  while _environments.is_connected:
    actions = _environments.action_space.sample()
    states = _environments.react(actions)
    state = next(iter(states.values()))
    terminated = state.terminated

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
