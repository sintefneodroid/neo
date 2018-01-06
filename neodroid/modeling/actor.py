from neodroid.messaging import create_motors


class Actor(object):
  def __init__(self, flat_actor):
    self._flat_actor = flat_actor

  def get_name(self):
    return self._flat_actor.ActorName()

  def get_alive(self):
    return self._flat_actor.Alive()

  def get_motor(self,key):
    if key in create_motors(self._flat_actor):
      return create_motors(self._flat_actor)[key]

  def get_motors(self):
    return create_motors(self._flat_actor)

  def __repr__(self):
    motors_str = ''.join([str(motor.__repr__()) for motor in
                          self.get_motors().values()])

    return '    <Actor>\n' + \
           '      <name>' + self.get_name().decode('utf-8') + '</name>\n' + \
           '      <alive>' + str(self.get_alive()) + '</alive>\n' + \
           '      <Motors>\n' + \
           motors_str + \
           '      </Motors>\n' + \
           '    </Actor>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
