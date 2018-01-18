import neodroid.messaging


class Observation(object):
  def __init__(self, observation_name, observation_space, observation_value):
    self._observation_space = observation_space
    self._observation_name = observation_name
    self._observation_value = observation_value

  @property
  def observation_name(self):
    return self._observation_name

  @property
  def observation_space(self):
    if self._observation_space:
      return neodroid.messaging.create_motion_space(self._observation_space)

  @property
  def observation_value(self):
    return self._observation_value

  def __repr__(self):
    return '    <Observer>\n' + \
           '      <observation_name>' + self._observation_name + '</observation_name>\n' + \
           '      <observation_space>' + str(self.observation_space) + '</observation_space>\n' + \
           '      <observation_value>' + str(self.observation_value) + '</observation_value>\n' + \
           '    </Observer>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
