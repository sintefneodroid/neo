import json

from .reaction_parameters import ReactionParameters


class Reaction(object):
  def __init__(self,
               motions=[],
               configurations=[],
               parameters=None,
               unobservables=None,
               displayables=None,
               environment_name='all',
               serialised_message=''):
    self._serialised_message = serialised_message
    self._environment_name = environment_name
    if parameters is None:
      parameters = ReactionParameters()
    self._parameters = parameters
    self._configurations = configurations
    self._motions = motions
    self._unobservables = unobservables
    self._displayables = displayables

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
  def displayables(self):
    return self._displayables

  @displayables.setter
  def displayables(self, displayables):
    self._displayables = displayables

  @property
  def unobservables(self):
    return self._unobservables

  @unobservables.setter
  def unobservables(self, unobservables):
    self._unobservables = unobservables

  @property
  def serialised_message(self):
    return self._serialised_message

  @serialised_message.setter
  def serialised_message(self, message):
    self._serialised_message = message

  def to_dict(self):
    return {
      '_configurations': [configuration.to_dict() for configuration in
                          self._configurations],
      '_motions':        [motion.to_dict() for motion in self._motions]
      }

  def to_json(self):
    return json.dumps(self.to_dict())

  def __repr__(self):
    return '<Reaction>\n' + \
           str(self._parameters) + \
           '  <configurations>\n' + str(self.configurations) + \
           '  </configurations>\n' + \
           '  <motions>\n' + str(self.motions) + \
           '  </motions>\n' + \
           '  <parameters>\n' + str(self.parameters) + \
           '  </parameters>\n' + \
           '  <configurations>\n' + str(self.configurations) + \
           '  </configurations>\n' + \
           '  <displayables>\n' + str(self.displayables) + \
           '  </displayables>\n' + \
           '  <unobservables>\n' + str(self.unobservables) + \
           '  </unobservables>\n' + \
           '  <serialised_message>\n' + str(self.serialised_message) + \
           '  </serialised_message>\n' + \
           '</Reaction>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
