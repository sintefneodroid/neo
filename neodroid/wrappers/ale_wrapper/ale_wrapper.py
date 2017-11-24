from neodroid import NeodroidEnvironment


class NeodroidALEWrapper(NeodroidEnvironment):
  def __init__(self, **kwargs):
    super(NeodroidALEWrapper, self).__init__(**kwargs)

  def act(self,
          input_reaction=None,
          on_step_done_callback=None,
          on_reaction_sent_callback=None):
    pass

  def reset_game(self, input_configuration=None):
    pass
