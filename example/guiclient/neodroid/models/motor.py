class Motor(object):
  _binary:bool
  _energi_cost:float
  _name:str

  def __init__(self, name, obj_tuple):
    self._name = name
    self.unpack(obj_tuple)

  def unpack(self, obj_tuple):
    self._binary = obj_tuple[0]
    self._energi_cost = obj_tuple[1]
