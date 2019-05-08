#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.wrappers import BinaryActionEncodingWrapper

__author__ = 'cnheider'

from pynput import keyboard


def up():
  return 0


def down():
  return 1


def left():
  return 2


def right():
  return 3


def reset():
  return 'reset'


_environments = BinaryActionEncodingWrapper(environment_name='grd', connect_to_running=False)
_environments.reset()

COMBINATIONS = {
  keyboard.KeyCode(char='w'):up,
  keyboard.KeyCode(char='s'):down,
  keyboard.KeyCode(char='a'):left,
  keyboard.KeyCode(char='d'):right,
  keyboard.KeyCode(char='r'):reset
  }

# The currently active modifiers
current_combinations = set()


def listen_for_combinations():
  print(f'\n\nPress any of:\n{COMBINATIONS}\n for early stopping\n')
  print('')
  return keyboard.Listener(on_press=on_press, on_release=on_release)


def on_press(key):
  if any([key in COMBINATIONS]):
    current_combinations.add(key)
    actions = COMBINATIONS[key]()
    terminated = False
    if _environments.is_connected:
      if actions == 'reset':
        obs = _environments.reset()
      else:
        obs, signal, terminated, _ = _environments.act(actions)
      # state = next(iter(states.values()))

      if terminated:
        _environments.reset()


def on_release(key):
  if any([key in COMBINATIONS]):
    current_combinations.remove(key)


if __name__ == '__main__':

  def main():

    with listen_for_combinations() as listener:
      listener.join()


  main()
