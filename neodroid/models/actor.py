from typing import List

from neodroid.models.motor import Motor


class Actor(object):
  _name: str
  _position: List[float]
  _rotation: List[float]
  _motors: List[Motor]

  def __init__(self, name, obj):
    self._name = name
    self._position = obj[0]
    self._rotation = obj[1]

  def get_position(self):
    return self._position

  def get_rotation(self):
    return self._rotation
