import json

from neodroid.models import Motion


class Reaction(object):
  def __init__(self, reset, configurations, motions):
    self._reset = reset
    self._configurations = configurations
    self._motions = motions

  def get_motions(self):
    return self._motions

  def set_motions(self, motions):
    self._motions = motions

  def get_configurations(self):
    return self._configurations

  def set_configurations(self, configurations):
    self._configurations = configurations

  def get_reset(self):
    return self._reset

  def to_dict(self):
    return {
      '_reset': self._reset,
      '_configurations': [configuration.to_dict() for configuration in self._configurations],
      '_motions': [motion.to_dict() for motion in self._motions]
    }

  def to_json(self):
    return json.dumps(self.to_dict())
