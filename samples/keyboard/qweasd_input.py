#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.wrappers import SingleEnvironmentWrapper

__author__ = 'cnheider'

from pynput import keyboard

_environments = SingleEnvironmentWrapper(connect_to_running=True)
_environments.reset()


def up():
  if 'ActorY_' in _environments.description.actuators:
    return {'ActorY_':_environments.description.actuator('ActorY_').motion_space.max}
  raise KeyError(f'Could not find actuator ActorY_')


def down():
  if 'ActorY_' in _environments.description.actuators:
    return {'ActorY_':_environments.description.actuator('ActorY_').motion_space.min}
  raise KeyError(f'Could not find actuator ActorY_')

def left():
  if 'ActorX_' in _environments.description.actuators:
    return {'ActorX_':_environments.description.actuator('ActorX_').motion_space.min}
  raise KeyError(f'Could not find actuator ActorX_')

def right():
  if 'ActorX_' in _environments.description.actuators:
    return {'ActorX_':_environments.description.actuator('ActorX_').motion_space.max}
  raise KeyError(f'Could not find actuator ActorX_')

def backward():
  if 'ActorZ_' in _environments.description.actuators:
    return {'ActorZ_':_environments.description.actuator('ActorZ_').motion_space.min}
  raise KeyError(f'Could not find actuator ActorZ_')

def forward():
  if 'ActorZ_' in _environments.description.actuators:
    return {'ActorZ_':_environments.description.actuator('ActorZ_').motion_space.max}
  raise KeyError(f'Could not find actuator ActorZ_')

def reset():
  return 'reset'


COMBINATIONS = {keyboard.KeyCode(char='q'):down,
                keyboard.KeyCode(char='w'):forward,
                keyboard.KeyCode(char='e'):up,
                keyboard.KeyCode(char='a'):right,
                keyboard.KeyCode(char='s'):backward,
                keyboard.KeyCode(char='d'):left,
                keyboard.KeyCode(char='x'):exit,
                keyboard.KeyCode(char='r'):reset
                }

# The currently active modifiers
current_combinations = set()


def listen_for_combinations():
  print(f'\n\nPress any of:\n{COMBINATIONS}\n\n')
  print('')
  return keyboard.Listener(on_press=on_press, on_release=on_release)


step_i = 0
auto_reset = False


def on_press(key):
  global step_i
  if any([key in COMBINATIONS]):
    if key not in current_combinations:
      current_combinations.add(key)
    actions = COMBINATIONS[key]()
    terminated = False
    signal = 0

    if _environments.is_connected:
      if actions == 'reset':
        obs = _environments.reset()
        step_i = 0
      else:
        obs, signal, terminated, _ = _environments.react(actions).to_gym_like_output()
      step_i += 1
      print('\n', step_i, obs, signal, terminated)

      if auto_reset and terminated:
        _environments.reset()
        step_i = 0


def on_release(key):
  if any([key in COMBINATIONS]):
    if key in current_combinations:
      current_combinations.remove(key)


def main():
  with listen_for_combinations() as listener:
    listener.join()


if __name__ == '__main__':

  main()
