import json


class Reaction(object):
  def __init__(self, reset, configurations, motions, environment_name='default'):
    self._environment_name = environment_name
    self._reset = reset
    self._configurations = configurations
    self._motions = motions

  def get_environment_name(self):
    return self._environment_name

  def get_reset(self):
    return self._reset

  def get_motions(self):
    return self._motions

  def set_motions(self, motions):
    self._motions = motions

  def get_configurations(self):
    return self._configurations

  def set_configurations(self, configurations):
    self._configurations = configurations

  def to_dict(self):
    return {
      '_reset'         : self._reset,
      '_configurations': [configuration.to_dict() for configuration in
                          self._configurations],
      '_motions'       : [motion.to_dict() for motion in self._motions]
    }

  def to_json(self):
    return json.dumps(self.to_dict())

  def __repr__(self):
    return '<Reaction>\n' + \
           '  <reset>\n' + str(self._reset) + '</reset>\n' + \
           '  <configurations>\n' + str(self._configurations) + '</configurations>\n' + \
           '  <motions>\n' + str(self._motions) + \
           '  </motions>\n' + \
           '</Reaction>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
