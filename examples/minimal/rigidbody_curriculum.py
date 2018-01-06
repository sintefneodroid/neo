# coding=utf-8
import neodroid.wrappers.curriculum_wrapper as neo
from neodroid import Configuration
import numpy as np

random_motion_horizon = 5
_memory = []
_sampled_initial_state_values = []


def get_goal_configuration(environment):
  _, _, _, message = environment.observe()
  if message:
    goal_transform = message.get_environment_description().get_configurable(b'GoalTransformX')
    if goal_transform:
      goal_transform = goal_transform.get_current_value()
      return [
      Configuration('LunarLanderTransformX', goal_transform[0][0]),
      Configuration('LunarLanderTransformY', goal_transform[0][1]),
      Configuration('LunarLanderTransformZ', goal_transform[0][2]),
      Configuration('LunarLanderTransformDirX', goal_transform[1][0]),
      Configuration('LunarLanderTransformDirY', goal_transform[1][1]),
      Configuration('LunarLanderTransformDirZ', goal_transform[1][2]),
      Configuration('LunarLanderTransformRotX', goal_transform[2][0]),
      Configuration('LunarLanderTransformRotY', goal_transform[2][1]),
      Configuration('LunarLanderTransformRotZ', goal_transform[2][2])]
    else:
      return [
      Configuration('SatelliteRigidbodyVelX', 0),
      Configuration('SatelliteRigidbodyVelY', 0),
      Configuration('SatelliteRigidbodyVelZ', 0),
      Configuration('SatelliteRigidbodyAngX', 0),
      Configuration('SatelliteRigidbodyAngY', 0),
      Configuration('SatelliteRigidbodyAngZ', 0)]

def main():
  _environment = neo.make('lunarlander', connect_to_running=False)
  _environment.seed(42)

  initial_configuration = get_goal_configuration(_environment)
  _memory.extend(_environment.generate_inital_states_from_goal_state(initial_configuration))

  for i in range(300):
      state = sample_initial_state(_memory)
      _environment.configure(state=state)

      if i % 20 == 19:
        new_initial_states = _environment.generate_inital_states_from_state(state)
        _memory.extend(new_initial_states)

      terminated= False
      while not terminated:
        actions = _environment.action_space.sample()
        observations, reward, terminated, info = _environment.act(actions)
        if terminated:
          print('Interrupted', reward)
          break

  _environment.close()

def sample_initial_state(memory):
  idx = np.random.randint(0,len(memory))
  return memory[idx]


if __name__ == '__main__':
  main()
