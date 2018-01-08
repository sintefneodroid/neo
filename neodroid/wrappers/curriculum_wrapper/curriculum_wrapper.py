from neodroid import NeodroidEnvironment
from neodroid.models import ReactionParameters, Reaction
from neodroid.utilities.statics import flattened_observation


class NeodroidCurriculumWrapper(NeodroidEnvironment):
  def __init__(self, *args, **kwargs):
    super(NeodroidCurriculumWrapper, self).__init__(*args, **kwargs)

  def __next__(self):
    if not self._connected_to_server:
      raise StopIteration
    return self.act()

  def act(self, *args, **kwargs):
    message = super(NeodroidCurriculumWrapper, self).react(*args, **kwargs)
    if message:
      return (flattened_observation(message),
              message.reward,
              message.terminated, message)

  def configure(self, *args, **kwargs):
    message = super(NeodroidCurriculumWrapper, self).reset(*args, **kwargs)
    if message:
      return flattened_observation(message), message

  def generate_inital_states_from_configuration(self, initial_configuration, motion_horizon=10, num=10):

    initial_states = []
    while len(initial_states) < num:
      params = ReactionParameters(terminable=False, episode_count=False, reset=True, configure=True)
      init = Reaction(params, initial_configuration)
      _, info = self.configure(init)

      params = ReactionParameters(terminable=False, episode_count=False, reset=False, configure=False,
                                  step=True)
      for i in range(motion_horizon):
        self.act(self.action_space.sample(), params)
      _, _, terminated, info = self.observe()
      if not terminated:
        initial_states.append(info)

    return initial_states

  def generate_inital_states_from_state(self, state, motion_horizon=10, num=10):
    initial_states = []
    params = ReactionParameters(terminable=True,
                                episode_count=False,
                                reset=False,
                                configure=False,
                                step=True)
    while len(initial_states) < num:
      _, info = self.configure(None, state)

      terminated = False
      for i in range(motion_horizon):
        _, _, terminated, info = self.act(self.action_space.sample(), params)
        if terminated:
          break
      if not terminated:
        initial_states.append(info)

    return initial_states

  def observe(self, *args, **kwargs):
    message = super(NeodroidCurriculumWrapper, self).observe()
    if message:
      return (flattened_observation(message),
              message.reward,
              message.terminated, message)

  def quit(self, *args, **kwargs):
    self.close(*args, **kwargs)
