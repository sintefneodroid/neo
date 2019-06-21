#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.wrappers.action_encoding_wrappers import DiscreteActionEncodingWrapper

__author__ = 'cnheider'

from pynput import keyboard


def up():
  return 2


def down():
  return 3


def left():
  return 1


def right():
  return 0


def reset():
  return 'reset'


_environments = DiscreteActionEncodingWrapper(environment_name='grd', connect_to_running=True)
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


step_i = 0
auto_reset = False


def on_press(key):
  global step_i
  if any([key in COMBINATIONS]):
    current_combinations.add(key)
    actions = COMBINATIONS[key]()
    terminated = False
    signal = 0

    if _environments.is_connected:
      if actions == 'reset':
        obs = _environments.reset()
        step_i = 0
      else:
        obs, signal, terminated, _ = _environments.step(actions)
      # state = next(iter(states.values()))
      step_i += 1
      print(step_i, obs, signal, terminated)

      if auto_reset and terminated:
        _environments.reset()
        step_i = 0


def on_release(key):
  if any([key in COMBINATIONS]):
    current_combinations.remove(key)


def main():
  with listen_for_combinations() as listener:
    listener.join()


if __name__ == '__main__':

  main()
