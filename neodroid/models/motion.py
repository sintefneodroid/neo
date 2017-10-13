class Motion(object):
  def __init__(self, actor_name, motor_name, strength):
    self._actor_name = actor_name
    self._motor_name = motor_name
    self._strength = strength  # Strength has a possible direction given by the sign of the float

  def get_actor_name(self):
    return self._actor_name

  def get_motor_name(self):
    return self._motor_name

  def get_strength(self):
    return self._strength

  def to_dict(self):
    return {'_actor_name': self._actor_name,
            '_motor_name': self._motor_name,
            '_strength': self._strength}
