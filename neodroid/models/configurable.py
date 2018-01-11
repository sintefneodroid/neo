# @pretty_print
class Configurable(object):
  def __init__(self, configurable_name, valid_range, observation):
    self._configurable_name = configurable_name
    self._valid_range = valid_range
    self._observation = observation

  @property
  def configurable_name(self):
    return self._configurable_name

  @property
  def valid_range(self):
    return self._valid_range

  @property
  def observation(self):
    return self._observation

  def to_dict(self):
    return {
      '_configurable_name' : self._configurable_name,
      '_configurable_value': self._valid_range
    }

  def __repr__(self):
    return '<Configurable>\n' + \
           '  <configurable_name>' + str(self._configurable_name) + \
           '</configurable_name>\n' + \
           '  <valid_range>\n' + str(self._valid_range) + \
           '</valid_range>\n' + \
           '  <current_value>\n' + str(self._observation) + \
           '</current_value>\n' + \
           '</Configurable>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
