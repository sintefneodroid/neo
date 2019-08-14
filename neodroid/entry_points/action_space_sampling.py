#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import time

from neodroid.environments import connect

__author__ = 'cnheider'


def add_bool_arg(parser, name, *, dest=None, default=False, **kwargs):
  if not dest:
    dest = name

  group = parser.add_mutually_exclusive_group(required=False)

  group.add_argument(f'--{name.upper()}', f'-{name.lower()}', dest=dest, action='store_true', **kwargs)
  group.add_argument(f'--NO-{name.upper()}', f'-no-{name.lower()}', dest=dest, action='store_false', **kwargs)
  parser.set_defaults(**{dest:default})


def main():
  parser = argparse.ArgumentParser(description='Neodroid Action Space Sampling')
  parser.add_argument('--IP',
                      '-ip',
                      type=str,
                      default='localhost',
                      metavar='IP',
                      help='IP Address')
  parser.add_argument('--PORT',
                      '-port',
                      type=int,
                      default=6969,
                      metavar='PORT',
                      help='Port')
  add_bool_arg(parser,
               'verbose',
               dest='VERBOSE',
               default=False,
               help='Verbose flag')

  args = parser.parse_args()

  environment = connect()

  i = 0
  freq = 100
  time_s = time.time()
  terminated = False
  while environment.is_connected:
    action = environment.action_space.sample()
    state = environment.react(action)
    for k, v in state.items():
      terminated = v.terminated
      break

    time_now = time.time()
    if i % freq == 0:
      fps = (1 / (time_now - time_s))
      print(f'fps:[{fps}]')

    i += 1
    time_s = time_now

    if terminated:
      environment.reset()


if __name__ == '__main__':
  main()