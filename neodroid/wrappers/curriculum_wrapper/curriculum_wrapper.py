from neodroid import NeodroidEnvironment
from neodroid.models import ReactionParameters, Reaction
from neodroid.utilities.statics import flattened_observation
import numpy as np

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
      return (np.array(flattened_observation(message)),
              message.signal,
              message.terminated, message)
    return None,None,None,None

  def configure(self, *args, **kwargs):
    message = super(NeodroidCurriculumWrapper, self).reset(*args, **kwargs)
    if message:
      return np.array(flattened_observation(message))
    return None,None

  def generate_initial_states_from_configuration(self, initial_configuration, motion_horizon=6, num=30):

    initial_states = []
    configure_params = ReactionParameters(terminable=False, episode_count=False, reset=True, configure=True)
    init = Reaction(configure_params, initial_configuration)

    while len(initial_states) < num:
      self.configure(init)

      for i in range(motion_horizon):
        _, _, terminated, info = self.act(self.action_space.sample())

        if not terminated:
          initial_states.append(info)

    return initial_states

  def generate_initial_states_from_state(self, state, motion_horizon=10, num=100):
    initial_states = []

    while len(initial_states) < num:
      self.configure(state=state)

      for i in range(motion_horizon):
        _, _, terminated, info = self.act(self.action_space.sample())

        if not terminated:
          initial_states.append(info)

    return initial_states

  def observe(self, *args, **kwargs):
    message = super(NeodroidCurriculumWrapper, self).observe()
    if message:
      return (flattened_observation(message),
              message.signal,
              message.terminated, message)
    return None,None,None,None

  def quit(self, *args, **kwargs):
    return self.close(*args, **kwargs)
