#!/usr/bin/env python3
# coding=utf-8
__author__='cnheider'
from tqdm import tqdm

import neodroid.wrappers.formal_wrapper as neo


def main():
  _environment = neo.make('grid_world', connect_to_running=False)

  observation_session = tqdm(_environment)
  for (observation, reward, terminated, info) in observation_session:
    if terminated:
      print('Interrupted', reward)

  _environment.close()


if __name__ == '__main__':
  main()
