from neodroid import NeodroidEnvironment
from neodroid.utilities.statics import flattened_observation


class NeodroidGymWrapper(NeodroidEnvironment):
  def __init__(self, **kwargs):
    super(NeodroidGymWrapper, self).__init__(**kwargs)
    self.observation_space = self.__observation_space__()
    self.action_space = self.__action_space__()

  def step(self, **kwargs):
    message = super(NeodroidGymWrapper, self).react(**kwargs)
    if message:
      return (flattened_observation(message),
              message.reward,
              message.terminated, message)
    return None, None, None, None

  def reset(self, **kwargs):
    message = super(NeodroidGymWrapper, self).reset(**kwargs)
    if message:
      return flattened_observation(message)
    return None

  def render(self, *args, **kwargs):
    pass

  def __next__(self):
    return self.step()
