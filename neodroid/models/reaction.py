from neodroid.models.motion import Motion
from typing import Dict
import json

class Reaction(object):
  _actor_motor_motions: Dict[str,Motion]
  _reset: bool

  def __init__(self):
    self._reset = True

  def to_dict(self):
    return {'_reset': self._reset, '_actor_motor_motions': {'GripperActor': Motion('GripperActor', 'SliderPart', 0.01).to_dict() }}

  def to_json(self):
    return json.dumps(self.to_dict())