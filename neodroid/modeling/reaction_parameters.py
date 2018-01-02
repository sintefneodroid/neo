import json


class ReactionParameters(object):
  def __init__(self, interruptible=True, step=False, reset = False,configure=False,describe=False):
    self._interruptible = interruptible
    self._configure = configure
    self._step = step
    self._reset = reset
    self._describe = describe

  def get_reset(self):
    return self._reset

  def get_configure(self):
    return self._configure

  def get_describe(self):
    return self._describe

  def get_step(self):
    return self._step

  def get_interruptible(self):
    return self._interruptible

  def to_dict(self):
    return {
      '_reset'         : self._reset
    }

  def to_json(self):
    return json.dumps(self.to_dict())

  def __repr__(self):
    return '<ReactionParameters>\n' + \
           '  <interruptible>' + str(self._interruptible) + '</interruptible>\n' + \
           '  <step>' + str(self._step) + '</step>\n' + \
           '  <reset>' + str(self._reset) + '</reset>\n' + \
           '  <configure>' + str(self._configure) + '</configure>\n' + \
           '  <describe>' + str(self._describe) + '</describe>\n' + \
           '</ReactionParameters>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
