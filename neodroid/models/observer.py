from typing import List

import io


class Observer(object):
  _name:str
  _data:bytearray
  _position:List[float]
  _rotation:List[float]

  def __init__(self,name,obj):
    self._name = name
    self._data = io.BytesIO(obj[1][0])

  def get_data(self):
    return self._data