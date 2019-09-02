#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from neodroid.environments.unity import connect

__author__ = 'Christian Heider Nielsen'
__doc__ = ''


if __name__ == '__main__':

  generate_num = 10
  if generate_num > 0:
    dt = []
    with connect() as env:
      for i, state in enumerate(env):
        if i >= generate_num:
          break

        state = state[list(state.keys())[0]]
        label = state.sensor('String').value
        ray = state.sensor('Ray').value

        print(label,ray)