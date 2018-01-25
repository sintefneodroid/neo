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

  def generate_trajectory_from_configuration(self, initial_configuration, motion_horizon=6, non_terminable_horizon = 10):
    configure_params = ReactionParameters(terminable=False, episode_count=False, reset=True, configure=True)
    init = Reaction(configure_params, initial_configuration)

    non_terminable_params = ReactionParameters(terminable=False, episode_count=False, reset=False,
                                             configure=False,step=True)

    initial_states = []
    self.configure()
    while len(initial_states) < 1:
      self.configure(init)
      for i in range(non_terminable_horizon):
        reac = Reaction(non_terminable_params, [], self.action_space.sample())
        _, _, terminated, info = self.act(reac)


      for i in range(motion_horizon):
        _, _, terminated, info = self.act(self.action_space.sample())

        if not terminated:
          initial_states.append(info)
      non_terminable_horizon+=1

    return initial_states

  def generate_trajectory_from_state(self, state, motion_horizon=10):
    initial_states = []
    self.configure()
    while len(initial_states) < 1:
      self.configure(state=state)

      for i in range(motion_horizon):
        _, _, terminated, info = self.act(self.action_space.sample())

        if not terminated:
          initial_states.append(info)
      motion_horizon += 1

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
