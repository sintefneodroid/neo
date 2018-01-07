import neodroid.messaging


class Actor(object):
  def __init__(self, flat_actor):
    self._flat_actor = flat_actor

  @property
  def name(self):
    return self._flat_actor.ActorName()

  @property
  def is_alive(self):
    return self._flat_actor.Alive()

  def motor(self, key):
    if key in neodroid.messaging.create_motors(self._flat_actor):
      return neodroid.messaging.create_motors(self._flat_actor)[key]

  @property
  def motors(self):
    return neodroid.messaging.create_motors(self._flat_actor)

  def __repr__(self):
    motors_str = ''.join([str(motor.__repr__()) for motor in
                          self.motors.values()])

    return '    <Actor>\n' + \
           '      <name>' + self.name.decode('utf-8') + '</name>\n' + \
           '      <alive>' + str(self.is_alive) + '</alive>\n' + \
           '      <Motors>\n' + \
           motors_str + \
           '      </Motors>\n' + \
           '    </Actor>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
