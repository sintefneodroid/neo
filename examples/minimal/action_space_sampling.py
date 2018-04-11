#!/usr/bin/env python3
# coding=utf-8

import neodroid.wrappers.formal_wrapper as neo


def main():
  _environment = neo.make('maze', connect_to_running=True)

  while _environment.is_connected:
    actions = _environment.action_space.sample()
    print(actions)
    _, reward, terminated, info = _environment.act(actions)
    if terminated:
      print(info.termination_reason)


if __name__ == '__main__':
  main()
