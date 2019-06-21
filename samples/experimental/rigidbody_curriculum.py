#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'
import numpy as np
from neodroid.models import Configuration

import neodroid.wrappers.curriculum_wrapper as neo

random_motion_horizon = 5
_memory = []
_sampled_initial_state_values = []


def get_goal_configuration(environment):
  _, _, _, message = environment.observe()
  if message and message.description:
    goal_transform = message.description.configurable('GoalEulerTransform')
    if goal_transform:
      goal_transform = goal_transform.configurable_value
      return [
        Configuration('LunarLanderEulerTransformX', goal_transform[0][0]),
        Configuration('LunarLanderEulerTransformY', goal_transform[0][1]),
        Configuration('LunarLanderEulerTransformZ', goal_transform[0][2]),
        Configuration('LunarLanderEulerTransformDirX', goal_transform[1][0]),
        Configuration('LunarLanderEulerTransformDirY', goal_transform[1][1]),
        Configuration('LunarLanderEulerTransformDirZ', goal_transform[1][2]),
        Configuration('LunarLanderEulerTransformRotX', goal_transform[2][0]),
        Configuration('LunarLanderEulerTransformRotY', goal_transform[2][1]),
        Configuration('LunarLanderEulerTransformRotZ', goal_transform[2][2]),
        ]
    else:
      return [
        Configuration('SatelliteRigidbodyVelX', 0),
        Configuration('SatelliteRigidbodyVelY', 0),
        Configuration('SatelliteRigidbodyVelZ', 0),
        Configuration('SatelliteRigidbodyAngX', 0),
        Configuration('SatelliteRigidbodyAngY', 0),
        Configuration('SatelliteRigidbodyAngZ', 0),
        ]


def main():
  _environment = neo.make('lunarlander', connect_to_running=False)
  _environment.seed(42)

  initial_configuration = get_goal_configuration(_environment)
  _memory.extend(
      _environment.generate_initial_states_from_configuration(initial_configuration)
      )

  for i in range(300):
    state = sample_initial_state(_memory)
    if not _environment.is_connected:
      break

    if i % 20 == 19:
      new_initial_states = _environment.generate_initial_states_from_state(state)
      _memory.extend(new_initial_states)
    _environment.configure(state=state)

    terminated = False
    while not terminated:
      actions = _environment.action_space._sample()
      observations, reward, terminated, info = _environment.act(actions)
      if terminated:
        print('Interrupted', reward)
        break

  _environment.close()


def sample_initial_state(memory):
  idx = np.random.randint(0, len(memory))
  return memory[idx]


if __name__ == '__main__':
  main()
