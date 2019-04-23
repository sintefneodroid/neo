#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import time

__author__ = 'cnheider'

import neodroid as neo


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

  environments = neo.make(verbose=False)
  environments.reset()

  i = 0
  freq = 100
  time_s = time.time()
  while environments.is_connected:
    actions = environments.action_space.sample()
    states = environments.react(actions)
    state = next(iter(states.values()))
    terminated = state.terminated

    time_now = time.time()
    if i % freq == 0:
      fps = (1 / (time_now - time_s))
      print(f'fps:[{fps}]')

    i += 1
    time_s = time_now

    if terminated:
      environments.reset()


if __name__ == '__main__':
  main()
