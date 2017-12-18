class Configurable(object):
  def __init__(self, configurable_name, valid_range, has_observer, observer_name):
    self._configurable_name = configurable_name
    self._valid_range = valid_range
    self._has_observer = has_observer
    self._observer_name = observer_name

  def get_configurable_name(self):
    return self._configurable_name

  def get_valid_range(self):
    return self._valid_range

  def get_observer_name(self):
    return self._observer_name

  def get_has_observer(self):
    return self._has_observer

  def to_dict(self):
    return {
      '_configurable_name' : self._configurable_name,
      '_configurable_value': self._valid_range
    }

  def __repr__(self):
    return '<Configurable>\n' + \
           '  <configurable_name>' + str(self._configurable_name) + \
           '</configurable_name>\n' + \
           '  <has_observer>' + str(self._has_observer) + \
           '</has_observer>\n' + \
           '  <observer_name>' + str(self._observer_name) + \
           '</observer_name>\n' + \
           '  <valid_range>\n' + str(self._valid_range) + \
           '</valid_range>\n' + \
           '</Configurable>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
