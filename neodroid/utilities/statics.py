import numpy as np

from neodroid.utilities.action_space import ActionSpace


def flattened_observation(message):
  flat = [obs.data for obs in message.observers.values() if obs.data is not None]
  flatter = np.hstack(flat).flatten()
  flatest = flatter
  return  flatest


def contruct_action_space(environment_description):
  valid_inputs = []
  for actor in environment_description.actors.values():
    for motor in actor.motors.values():
      valid_inputs.append(motor.valid_input)
  return ActionSpace(valid_inputs)
