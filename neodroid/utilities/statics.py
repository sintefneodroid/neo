import numpy as np

from neodroid.utilities.action_space import ActionSpace


def flattened_observation(message):
  return np.array([obs.get_data() for obs in message.get_observers().values()]).flatten()


def contruct_action_space(environment_description):
  valid_inputs = []
  for actor in environment_description.get_actors().values():
    for motor in actor.get_motors().values():
      valid_inputs.append(motor.get_valid_input())
  return ActionSpace(valid_inputs)
