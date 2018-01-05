from neodroid import NeodroidEnvironment
from neodroid.utilities.statics import flattened_observation


class NeodroidFormalWrapper(NeodroidEnvironment):
  def __init__(self, **kwargs):
    super(NeodroidFormalWrapper, self).__init__(**kwargs)
    self.observation_space = self.__observation_space__()
    self.action_space = self.__action_space__()

  def act(self,
          input_reaction=None,
          on_step_done_callback=None,
          on_reaction_sent_callback=None):
    message = super(NeodroidFormalWrapper, self).react(input_reaction,
                                                       on_reaction_sent_callback,
                                                       on_step_done_callback)
    if message:
      return (flattened_observation(message),
              message.get_reward(),
              message.get_terminated(), message)
    return None, None, None, None

  def configure(self, input_configuration=[], on_reset_callback=None):
    message = super(NeodroidFormalWrapper, self).reset(input_configuration,
                                                       on_reset_callback)
    if message:
      return flattened_observation(message), message
    return None, None

  def observe(self):
    message = super(NeodroidFormalWrapper, self).observe()
    if message:
      return (flattened_observation(message),
              message.get_reward(),
              message.get_terminated(), message)


  def quit(self, callback=None):
    self.close(callback=callback)
