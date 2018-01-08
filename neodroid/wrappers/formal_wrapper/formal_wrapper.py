from neodroid import NeodroidEnvironment
from neodroid.utilities.statics import flattened_observation


class NeodroidFormalWrapper(NeodroidEnvironment):
  def __init__(self, **kwargs):
    super(NeodroidFormalWrapper, self).__init__(**kwargs)

  def __next__(self):
    if not self._connected_to_server:
      raise StopIteration
    return self.act()

  def act(self, *args, **kwargs):
    message = super(NeodroidFormalWrapper, self).react(*args, **kwargs)
    if message:
      return (flattened_observation(message),
              message.reward,
              message.terminated, message)

  def configure(self,*args, **kwargs):
    message = super(NeodroidFormalWrapper, self).reset(*args, **kwargs)
    if message:
      return flattened_observation(message), message

  def observe(self,*args, **kwargs):
    message = super(NeodroidFormalWrapper, self).observe(*args, **kwargs)
    if message:
      return (flattened_observation(message),
              message.reward,
              message.terminated, message)

  def quit(self,*args, **kwargs):
    self.close(*args, **kwargs)
