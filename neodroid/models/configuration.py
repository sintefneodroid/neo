class Configuration(object):
  def __init__(self, configurable_name, configurable_value):
    self._configurable_name = configurable_name
    self._configurable_value = configurable_value

  def get_configurable_name(self):
    return self._configurable_name

  def get_configurable_value(self):
    return self._configurable_value

  def to_dict(self):
    return {
      '_configurable_name': self._configurable_name,
      '_configurable_value'  : self._configurable_value
    }
