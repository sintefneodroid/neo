# coding=utf-8
import numpy as np

import neodroid.wrappers.curriculum_wrapper as neo
from neodroid.models import Configuration

random_motion_horizon = 5
_memory = []
_sampled_initial_state_values = []


def get_goal_configuration(environment):
  if environment:
    goal_pos = environment.description.configurable('GoalPosition').current_value
    return goal_pos


def main():
  _environment = neo.make('3d_grid_world', connect_to_running=False)
  _environment.seed(42)

  goal_pos = get_goal_configuration(_environment)


  initial_configuration = [Configuration('ActorPositionX', goal_pos[0]),
                           Configuration('ActorPositionY', goal_pos[1]),
                           Configuration('ActorPositionZ', goal_pos[2])]
  _memory.extend(_environment.generate_inital_states_from_configuration(initial_configuration))

  for i in range(300):
    state = sample_initial_state(_memory)
    if not _environment.is_connected:
      break

    if i % 20 == 19:
      _memory.extend(_environment.generate_inital_states_from_state(state))

    _environment.configure(state=state)



    terminated = False
    while not terminated:
      actions = _environment.action_space.sample()
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
