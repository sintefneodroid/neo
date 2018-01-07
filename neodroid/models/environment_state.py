import neodroid.messaging


# @pretty_print
class EnvironmentState(object):
  def __init__(self, fbs_state):
    self._fbs_state = fbs_state

  @property
  def environment_name(self):
    return self._fbs_state.EnvironmentName()

  @property
  def reward(self):
    return self._fbs_state.Reward()

  @property
  def unobservables(self):
    return neodroid.messaging.create_unobservables(self._fbs_state)

  @property
  def frame_number(self):
    return self._fbs_state.FrameNumber()

  @property
  def terminated(self):
    return self._fbs_state.Terminated()

  @property
  def total_energy_spent_since_reset(self):
    return self._fbs_state.TotalEnergySpent()

  @property
  def description(self):
    if self._fbs_state.EnvironmentDescription():
      return neodroid.messaging.create_description(self._fbs_state.EnvironmentDescription())

  @property
  def observers(self):
    return neodroid.messaging.create_observers(self._fbs_state)

  def observer(self, key):
    if key in neodroid.messaging.create_observers(self._fbs_state):
      return neodroid.messaging.create_observers(self._fbs_state)[key]

  def __repr__(self):
    observers_str = ''.join([
      str(observer.__repr__()) for observer in self.observers.values()
    ])

    description_str = str(self.description)
    return '<EnvironmentState>\n' + \
           '  <total_energy_spent>' + \
           str(self.total_energy_spent_since_reset) + \
           '</total_energy_spent>\n' + \
           '  <frame_number>' + \
           str(self.frame_number) + \
           '</frame_number>\n' + \
           '  <reward>' + \
           str(self.reward) + \
           '</reward>\n' + \
           '  <interrupted>' + \
           str(self.terminated) + \
           '</interrupted>\n' + \
           '  <Observers>\n' + \
           observers_str + \
           '  </Observers>\n' + \
           str(self.description) + \
           str(self.unobservables) + \
           '</EnvironmentState>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
