from neodroid.models.motion import Motion
from typing import List
import json

class Reaction(object):
  #_actor_motor_motions: List[Motion]
  #_reset: bool

  def __init__(self, reset, actor_motor_motions):
    self._reset = reset
    self._actor_motor_motions = actor_motor_motions

  def to_dict(self):
    return {'_reset': self._reset, '_actor_motor_motions': [motion.to_dict() for motion in self._actor_motor_motions]}

  def to_json(self):
    return json.dumps(self.to_dict())