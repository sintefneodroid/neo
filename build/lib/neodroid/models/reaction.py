import json
from typing import List

from neodroid.models.motion import Motion


class Reaction(object):
  # _actor_motor_motions: List[Motion]
  # _reset: bool

  def __init__(self, reset, motions):
    self._reset = reset
    self._motions = motions

  def to_dict(self):
    return {'_reset'              : self._reset,
            '_actor_motor_motions': [motion.to_dict() for motion in
                                     self._motions]}

  def to_json(self):
    return json.dumps(self.to_dict())
