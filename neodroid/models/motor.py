class Motor(object):
  #_binary:bool
  #_energy_cost:float
  #_name:str

  def __init__(self, name, obj_tuple):
    self._name = name
    self.unpack(obj_tuple)

  def unpack(self, obj_tuple):
    self._binary = obj_tuple[0]
    self._energy_cost = obj_tuple[1]

  def __repr__(self):
    return  '        <Motor>\n'+\
            '          <name>'+ self._name.decode('utf-8')+'</name>\n'+ \
            '          <binary>' + str(self._binary) + '</binary>\n' + \
            '          <energy_cost>' + str(self._energy_cost) + '</energy_cost>\n' + \
            '        </Motor>\n'


  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()