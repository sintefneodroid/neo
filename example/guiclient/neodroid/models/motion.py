class Motion(object):
  _actor_name:str
  _motor_name:str
  _strength:float #Strength has a possible direction given by the sign of the float

  def __init__(self, actor_name, motor_name, strength):
    self._actor_name = actor_name
    self._motor_name = motor_name
    self._strength = strength

  def to_dict(self):
    return {'_actor_name': self._actor_name,
            '_motor_name': self._motor_name,
            '_strength': self._strength}