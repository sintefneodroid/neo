class Observer(object):
  def __init__(self, name, data):
    self._name = name
    self._data = data

  def get_name(self):
    return self._name

  def get_data(self):
    return self._data

  def __repr__(self):
    return '    <Observer>\n' + \
           '      <name>' + self._name.decode('utf-8') + '</name>\n' + \
           '      <data_sample>' + str(self._data) + '</data_sample>\n' + \
           '      <data_size>' + \
           str(self._data.__sizeof__()) + '</data_size>\n' + \
           '    </Observer>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
