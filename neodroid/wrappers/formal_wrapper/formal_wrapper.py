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
              message.signal,
              message.terminated, message)
    return None,None,None,None

  def configure(self,*args, **kwargs):
    message = super(NeodroidFormalWrapper, self).reset(*args, **kwargs)
    if message:
      return flattened_observation(message), message
    return None,None

  def observe(self,*args, **kwargs):
    message = super(NeodroidFormalWrapper, self).observe(*args, **kwargs)
    if message:
      return (flattened_observation(message),
              message.signal,
              message.terminated, message)
    return None,None,None,None

  def quit(self,*args, **kwargs):
    return self.close(*args, **kwargs)
