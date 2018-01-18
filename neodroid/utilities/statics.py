import numpy as np
import _io
from neodroid.utilities.action_space import ActionSpace
from neodroid.utilities.observation_space import ObservationSpace


def flattened_observation(message):
  #flat = np.array([np.hstack([obs.observation_value]).flatten() for obs in message.observers.values() if obs.observation_value is not None and type(obs.observation_value) is not _io.BytesIO])
  #flatter = np.hstack(flat).flatten()
  #flatter = np.hstack(flatter).flatten()
  #flatest = np.nan_to_num(flatter).tolist()
  obs = message.observables
  return obs

def contruct_action_space(environment_description):
  motion_spaces = []
  for actor in environment_description.actors.values():
    for motor in actor.motors.values():
      motion_spaces.append(motor.motion_space)
  return ActionSpace(motion_spaces)

def contruct_observation_space(state):
  return ObservationSpace(state)
