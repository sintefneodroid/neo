import json

from neodroid.modeling.reaction_parameters import ReactionParameters


class Reaction(object):
  def __init__(self, parameters,configurations=[], motions=[], environment_name='all'):
    self._environment_name = environment_name
    self._parameters = parameters
    self._configurations = configurations
    self._motions = motions

  def get_environment_name(self):
    return self._environment_name

  def get_parameters(self):
    return self._parameters

  def set_parameters(self, parameters):
    self._parameters = parameters

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
      '_configurations': [configuration.to_dict() for configuration in
                          self._configurations],
      '_motions'       : [motion.to_dict() for motion in self._motions]
    }

  def to_json(self):
    return json.dumps(self.to_dict())

  def __repr__(self):
    return '<Reaction>\n' + \
          str(self._parameters)+\
           '  <configurations>\n' + str(self._configurations) +\
           '  </configurations>\n' + \
           '  <motions>\n' + str(self._motions) + \
           '  </motions>\n' + \
           '</Reaction>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
