import numpy as np

from neodroid.messaging import create_observers, create_description, create_poses, create_bodies


class EnvironmentState(object):
  def __init__(self, fbs_state):
    self._fbs_state = fbs_state

  def get_environment_name(self):
    self._fbs_state.EnvironmentName()

  def get_reward(self):
    return self._fbs_state.Reward()

  def get_fbs_state(self):
    return self._fbs_state

  def get_poses_numpy(self):
    return create_poses(self._fbs_state)

  def get_bodies_numpy(self):
    return create_bodies(self._fbs_state)

  def get_frame_number(self):
    return self._fbs_state.FrameNumber()

  def get_state_configuration(self):
    return np.array([self.get_poses_numpy().flatten(), self.get_bodies_numpy().flatten()]).flatten()

  def get_terminated(self):
    return self._fbs_state.Terminated()

  def get_total_energy_spent_since_reset(self):
    return self._fbs_state.TotalEnergySpent()

  def get_environment_description(self):
    if self._fbs_state.EnvironmentDescription():
      return create_description(self._fbs_state.EnvironmentDescription())

  def get_observers(self):
    return create_observers(self._fbs_state)

  def get_observer(self, key):
    return create_observers(self._fbs_state)[key]

  def __repr__(self):
    observers_str = ''.join([
      str(observer.__repr__()) for observer in self.get_observers().values()
    ])

    description_str = str(self.get_environment_description())
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
           str(self.get_terminated()) + \
           '</interrupted>\n' + \
           '  <Poses>\n' + \
           str(self.get_poses_numpy()) + \
           '  </Poses>\n' + \
           '  <Bodies>\n' + \
           str(self.get_bodies_numpy()) + \
           '  </Bodies>\n' + \
           '  <Observers>\n' + \
           observers_str + \
           '  </Observers>\n' + \
           description_str + \
           '</EnvironmentState>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
