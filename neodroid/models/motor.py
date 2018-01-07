import neodroid.messaging


class Motor(object):
  def __init__(self, name, valid_input, energy_spent):
    self._name = name
    self._valid_input = valid_input
    self._energy_spent = energy_spent

  @property
  def name(self):
    return self._name

  @property
  def valid_input(self):
    return neodroid.messaging.create_valid_range(self._valid_input)

  @property
  def energy_spent(self):
    return self._energy_spent

  def __repr__(self):
    return '        <Motor>\n' + \
           '          <name>' + str(self._name.decode('utf-8')) + \
           '</name>\n' + \
           '          <valid_input>' + str(self._valid_input) + \
           '</valid_input>\n' + \
           '          <energy_spent>' + str(self._energy_spent) + \
           '</energy_spent>\n' + \
           '        </Motor>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
