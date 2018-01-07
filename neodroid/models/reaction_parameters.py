import json


class ReactionParameters(object):
  def __init__(self, terminable=True, step=False, reset=False, configure=False, describe=False,
               episode_count=True):
    self._terminable = terminable
    self._configure = configure
    self._step = step
    self._reset = reset
    self._describe = describe
    self._episode_count = episode_count

  @property
  def reset(self):
    return self._reset

  @property
  def configure(self):
    return self._configure

  @property
  def describe(self):
    return self._describe

  @property
  def step(self):
    return self._step

  @property
  def episode_count(self):
    return self._episode_count

  @property
  def terminable(self):
    return self._terminable

  def to_dict(self):
    return {
      '_reset': self._reset
    }

  def to_json(self):
    return json.dumps(self.to_dict())

  def __repr__(self):
    return '<ReactionParameters>\n' + \
           '  <terminable>' + str(self._terminable) + '</terminable>\n' + \
           '  <step>' + str(self._step) + '</step>\n' + \
           '  <reset>' + str(self._reset) + '</reset>\n' + \
           '  <configure>' + str(self._configure) + '</configure>\n' + \
           '  <describe>' + str(self._describe) + '</describe>\n' + \
           '  <episode_count>' + str(self._episode_count) + '</episode_count>\n' + \
           '</ReactionParameters>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
