#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from contextlib import suppress

__author__ = 'cnheider'
from tqdm import tqdm

tqdm.monitor_interval = 0

from neodroid.wrappers import NeodroidFormalWrapper


def main():
  frame_i = 0
  update_description_interval = 100

  appended_text = ''
  diverged = False
  with suppress(ConnectionError, KeyboardInterrupt), NeodroidFormalWrapper(connect_to_running=True) as env:
    with tqdm(env,
              leave=False) as observation_session:
      for (observation, reward, terminated, info) in observation_session:
        frame_i += 1

        if not diverged and frame_i != info.frame_number:
          appended_text += ', Diverged!'
          diverged = True
        if frame_i % update_description_interval == 0:
          observation_session.set_description(
              f'Local frame: {frame_i}, Unity frame: {info.frame_number}' + appended_text)

        if terminated:
          print(f'Interrupted, Length: {frame_i}, Unity frame: {info.frame_number}')
          env.reset()
          frame_i = 0
          appended_text = ''
          diverged = False


if __name__ == '__main__':
  main()
