import json


class Reaction(object):
  def __init__(self,
               parameters,
               configurations=[],
               motions=[],
               unobservables=None,
               environment_name='all'):
    self._environment_name = environment_name
    self._parameters = parameters
    self._configurations = configurations
    self._motions = motions
    self._unobservables = unobservables

  @property
  def environment_name(self):
    return self._environment_name

  @property
  def parameters(self):
    return self._parameters

  @parameters.setter
  def parameters(self, parameters):
    self._parameters = parameters

  @property
  def motions(self):
    return self._motions

  @motions.setter
  def motions(self, motions):
    self._motions = motions

  @property
  def configurations(self):
    return self._configurations

  @configurations.setter
  def configurations(self, configurations):
    self._configurations = configurations

  @property
  def unobservables(self):
    return self._unobservables

  @unobservables.setter
  def unobservables(self, unobservables):
    self._unobservables = unobservables

  def to_dict(self):
    return {
      '_configurations': [configuration.to_dict() for configuration in
                          self._configurations],
      '_motions'       : [motion.to_dict() for motion in self._motions]
    }

  def to_json(self):
    return json.dumps(self.to_dict())

  def __repr__(self):
    return '<Reaction>\n' + \
           str(self._parameters) + \
           '  <configurations>\n' + str(self._configurations) + \
           '  </configurations>\n' + \
           '  <motions>\n' + str(self._motions) + \
           '  </motions>\n' + \
           str(self.unobservables()) + \
           '</Reaction>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
