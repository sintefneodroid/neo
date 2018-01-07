# coding=utf-8
import numpy as np

import neodroid.wrappers.curriculum_wrapper as neo
from neodroid import Configuration

random_motion_horizon = 5
_memory = []
_sampled_initial_state_values = []


def get_goal_configuration(environment):
  _, _, _, message = environment.observe()
  if message:
    goal_x = message.description().configurable(b'GoalTransformX').current_value()
    goal_y = message.description().configurable(b'GoalTransformY').current_value()
    goal_z = message.description().configurable(b'GoalTransformZ').current_value()
    return goal_z


def main():
  _environment = neo.make('grid_world', connect_to_running=False)
  _environment.seed(42)

  goal_pos = get_goal_configuration(_environment)
  initial_configuration = [Configuration('ActorTransformX', goal_pos[0]),
                           Configuration('ActorTransformY', goal_pos[1]),
                           Configuration('ActorTransformZ', goal_pos[2])]
  _memory.extend(_environment.generate_inital_states_from_goal_state(initial_configuration))

  for i in range(300):
    state = sample_initial_state(_memory)
    if not _environment.is_connected():
      break
    _environment.configure(state=state)

    if i % 20 == 19:
      new_initial_states = _environment.generate_inital_states_from_state(state)
      _memory.extend(new_initial_states)

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
