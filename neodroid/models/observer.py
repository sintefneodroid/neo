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

  def __repr__(self):
    return '    <Observer>\n' + \
           '      <name>' + self._name.decode('utf-8') + '</name>\n' + \
           '      <position>' + str(self._position) + '</position>\n' + \
           '      <rotation>' + str(self._rotation) + '</rotation>\n' + \
           '      <data_size>' + str(self._data.__sizeof__()) + '</data_size>\n'+\
           '    </Observer>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()