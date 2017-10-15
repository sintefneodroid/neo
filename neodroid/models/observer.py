class Observer(object):
  def __init__(self, name, data, position, rotation, direction):
    self._name = name
    self._data = data
    self._position = position
    self._rotation = rotation
    self._direction = direction

  def get_name(self):
    return self._name

  def get_position(self):
    return self._position

  def get_rotation(self):
    return self._rotation

  def get_direction(self):
    return self._direction

  def get_data(self):
    return self._data

  def __repr__(self):
    return '    <Observer>\n' + \
           '      <name>' + self._name.decode('utf-8') + '</name>\n' + \
           '      <position>' + str(self._position) + '</position>\n' + \
           '      <rotation>' + str(self._rotation) + '</rotation>\n' + \
           '      <direction>' + str(self._direction) + '</direction>\n' + \
           '      <data_sample>' + str(self._data.getvalue()[:10]) + \
           '..' + str(self._data.getvalue()[-10:]) + '</data_sample>\n' + \
           '      <data_size>' + \
           str(self._data.__sizeof__()) + '</data_size>\n' + \
           '    </Observer>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
