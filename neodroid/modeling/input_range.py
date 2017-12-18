class InputRange(object):
  def __init__(self, decimal_granularity, min_value, max_value):
    self._decimal_granularity = decimal_granularity
    self._min_value = min_value
    self._max_value = max_value

  def get_decimal_granularity(self):
    return self._decimal_granularity

  def get_min_value(self):
    return self._min_value

  def get_max_value(self):
    return self._max_value

  def to_dict(self):
    return {
      '_configurable_name' : self._configurable_name,
      '_configurable_value': self._valid_range
    }

  def __repr__(self):
    return '<InputRange>\n' + \
           '  <decimal_granularity>' + str(self._decimal_granularity) + \
           '</decimal_granularity>\n' + \
           '  <min_value>' + str(self._min_value) + \
           '</min_value>\n' + \
           '  <max_value>' + str(self._max_value) + \
           '</max_value>\n' + \
           '</InputRange>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
