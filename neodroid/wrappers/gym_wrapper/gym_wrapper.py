import numpy as np

from neodroid import NeodroidEnvironment
from neodroid.utilities.statics import flattened_observation

class NeodroidGymWrapper(NeodroidEnvironment):
  def __init__(self, *args, **kwargs):
    super(NeodroidGymWrapper, self).__init__(*args, **kwargs)

  def step(self, action, *args, **kwargs):
    #action = action.flatten()
    message = super(NeodroidGymWrapper, self).react(action, *args, **kwargs)
    if message:
      return (np.array(flattened_observation(message)),
              message.signal,
              message.terminated, message)
    return None, None, None, None

  def reset(self, *args, **kwargs):
    message = super(NeodroidGymWrapper, self).reset(*args, **kwargs)
    if message:
      return np.array(flattened_observation(message))
    return None

  def render(self, *args, **kwargs):
    pass

  def __next__(self):
    if not self._connected_to_server:
      raise StopIteration
    return self.step()
