import neodroid.messaging


class Motor(object):
  def __init__(self, motor_name, motion_space, energy_spent):
    self._motor_name = motor_name
    self._motion_space = motion_space
    self._energy_spent = energy_spent

  @property
  def motor_name(self):
    return self._motor_name

  @property
  def motion_space(self):
    return neodroid.messaging.create_motion_space(self._motion_space)

  @property
  def energy_spent(self):
    return self._energy_spent

  def __repr__(self):
    return '        <Motor>\n' + \
           '          <name>' + self.motor_name + '</name>\n' + \
           '          <motion_space>' + str(self.motion_space) +  '</motion_space>\n' + \
           '          <energy_spent>' + str(self.energy_spent) + '</energy_spent>\n' + \
           '        </Motor>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
