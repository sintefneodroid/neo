#!/usr/bin/env python3
# coding=utf-8
__author__ = 'cnheider'

import neodroid.wrappers.formal_wrapper as neo


def main():
  _environments = neo.make('multienv', connect_to_running=True)
  _environments.reset()
  while _environments.is_connected:
    actions = _environments.action_space.sample()
    print(actions)
    observations, rewards, terminated, infos = _environments.act(actions)

    if terminated:
      _environments.reset()


if __name__ == '__main__':
  main()
