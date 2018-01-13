import numpy as np

from neodroid.utilities.action_space import ActionSpace


def flattened_observation(message):
  flat = [obs.observation_value for obs in message.observers.values() if obs.observation_value is not None]
  flatter = np.hstack(flat).flatten().astype(np.float)
  flatest = np.nan_to_num(flatter).tolist()
  return  flatest


def contruct_action_space(environment_description):
  valid_inputs = []
  for actor in environment_description.actors.values():
    for motor in actor.motors.values():
      valid_inputs.append(motor.motion_space)
  return ActionSpace(valid_inputs)
