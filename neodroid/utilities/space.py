class Space(object):
  def __init__(self, **kwargs):
    pass

  def sample(self):
    raise NotImplementedError

  def flat_size(self):
    raise NotImplementedError

  def size(self):
    raise NotImplementedError
