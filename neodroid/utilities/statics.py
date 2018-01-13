import numpy as np

from neodroid.utilities.action_space import ActionSpace
from neodroid.utilities.observation_space import ObservationSpace


def flattened_observation(message):
  flat = [obs.observation_value for obs in message.observers.values() if obs.observation_value is not None]
  flatter = np.hstack(flat).flatten().astype(np.float)
  flatest = np.nan_to_num(flatter).tolist()
  return  flatest

def contruct_action_space(environment_description):
  motion_spaces = []
  for actor in environment_description.actors.values():
    for motor in actor.motors.values():
      motion_spaces.append(motor.motion_space)
  return ActionSpace(motion_spaces)

def contruct_observation_space(state):
  return ObservationSpace(state)
