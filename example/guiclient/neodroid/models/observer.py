from typing import List

import io


class Observer(object):
  _name:str
  _data:bytearray
  _position:List[float]
  _rotation:List[float]

  def __init__(self,name,obj):
    self._name = name
    self.unpack(obj)

  def unpack(self, obj_tuple):
    self._data = io.BytesIO(obj_tuple[0])
    self._position = obj_tuple[1]
    self._rotation = obj_tuple[2]


  def get_data(self):
    return self._data