from typing import List

from neodroid.models.motor import Motor


class Actor(object):
  _name: str
  _position: List[float]
  _rotation: List[float]
  _motors: List[Motor]

  def __init__(self, name, obj_tuple):
    self._name = name
    self.unpack(obj_tuple)

  def unpack(self, obj_tuple):
    self._position = obj_tuple[1]
    self._rotation = obj_tuple[2]
    self._motors = {key: Motor(key,motor) for (key,motor) in obj_tuple[0][1].items()}

  def get_position(self):
    return self._position

  def get_rotation(self):
    return self._rotation
