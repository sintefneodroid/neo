class Actor(object):
  def __init__(self, name, position, rotation, motors):
    self._name = name
    self._position = position
    self._rotation = rotation
    self._motors = motors

  def get_name(self):
    return self._name

  def get_position(self):
    return self._position

  def get_rotation(self):
    return self._rotation

  def get_motors(self):
    return self._motors

  def __repr__(self):
    motors_str = ''.join([str(motor.__repr__()) for motor in self.get_motors()])

    return '    <Actor>\n' + \
           '      <name>' + self._name.decode('utf-8') + '</name>\n' + \
           '      <position>' + str(self._position) + '</position>\n' + \
           '      <rotation>' + str(self._rotation) + '</rotation>\n' + \
           '      <Motors>\n' + \
           motors_str + \
           '      </Motors>\n' + \
           '    </Actor>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
