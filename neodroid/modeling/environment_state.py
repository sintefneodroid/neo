from neodroid.messaging.FBSUtilities import create_actors, create_observers, \
  create_configurables


class EnvironmentState(object):
  def __init__(self, fbs_state):
    self._fbs_state = fbs_state

  def get_total_energy_spent_since_reset(self):
    return self._fbs_state.TotalEnergySpentSinceReset()

  def get_actors(self):
    return create_actors(self._fbs_state)

  def get_actor(self, key):
    return create_actors(self._fbs_state)[key]

  def get_observers(self):
    return create_observers(self._fbs_state)

  def get_observer(self, key):
    return create_observers(self._fbs_state)[key]

  def get_configurables(self):
    return create_configurables(self._fbs_state)

  def get_configurable(self, key):
    return create_configurables(self._fbs_state)[key]

  def get_reward(self):
    return self._fbs_state.Reward()

  def get_frame_number(self):
    return self._fbs_state.FrameNumber()

  def get_interrupted(self):
    return self._fbs_state.Interrupted()

  def __repr__(self):
    observers_str = ''.join([
      str(observer.__repr__()) for observer in create_observers(self._fbs_state).values()
    ])
    actors_str = ''.join(
        [str(actor.__repr__()) for actor in create_actors(self._fbs_state).values()])

    return '<EnvironmentState>\n' + \
           '  <total_energy_spent>' + \
           str(self.get_total_energy_spent_since_reset()) + \
           '</total_energy_spent>\n' + \
           '  <frame_number>' + \
           str(self.get_frame_number()) + \
           '</frame_number>\n' + \
           '  <reward>' + \
           str(self.get_reward()) + \
           '</reward>\n' + \
           '  <interrupted>' + \
           str(self.get_interrupted()) + \
           '</interrupted>\n' + \
           '  <Actors>\n' + \
           actors_str + \
           '  </Actors>\n' + \
           '  <Observers>\n' + \
           observers_str + \
           '  </Observers>\n' + \
           '</EnvironmentState>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
