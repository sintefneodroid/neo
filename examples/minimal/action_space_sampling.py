#!/usr/bin/env python3
# coding=utf-8
__author__ = 'cnheider'

import neodroid.wrappers.formal_wrapper as neo


def main():
  _environment = neo.make('multienv', connect_to_running=True)
  _environment.reset()
  while _environment.is_connected:
    actions = _environment.action_space.sample()
    print(actions)
    _, reward, terminated, info = _environment.act(actions)
    if terminated:
      print(info.termination_reason)
      _environment.reset()


if __name__ == '__main__':
  main()
