from neodroid import NeodroidEnvironment


class NeodroidGymWrapper(NeodroidEnvironment):
  def __init__(self, **kwargs):
    super(NeodroidGymWrapper, self).__init__(**kwargs)
    self.observation_space = self.__observation_space__()
    self.action_space = self.__action_space__()

  def step(self,
           input_reaction=None,
           on_reaction_sent_callback=None,
           on_step_done_callback=None):
    message = super(NeodroidGymWrapper, self).react(input_reaction,
                                                    on_reaction_sent_callback,
                                                    on_step_done_callback)
    if message:
      return (flat_observation(message),
              message.get_reward(),
              message.get_terminated(), message)
    return None, None, None, None

  def reset(self, input_configuration=[], on_reset_callback=None):
    message = super(NeodroidGymWrapper, self).reset(input_configuration,
                                                    on_reset_callback)
    if message:
      return flat_observation(message)
    return None

  def render(self, *args, **kwargs):
    pass
