from neodroid import NeodroidEnvironment


class NeodroidFormalWrapper(NeodroidEnvironment):
  def __init__(self, **kwargs):
    super(NeodroidFormalWrapper, self).__init__(**kwargs)

  def act(self,
          input_reaction=None,
          on_step_done_callback=None,
          on_reaction_sent_callback=None):
    return self.react(input_reaction=input_reaction,
                      on_step_done_callback=on_step_done_callback,
                      on_reaction_sent_callback=on_reaction_sent_callback)

  def configure(self, input_configuration=None):
    return self.reset(input_configuration)

  def quit(self, callback=None):
    self.close(callback=callback)
