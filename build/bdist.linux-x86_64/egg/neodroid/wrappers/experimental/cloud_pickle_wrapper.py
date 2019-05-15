import pickle as pk

import cloudpickle as cpk


class CloudPickleWrapper(object):
  """
  Uses cloudpickle to serialize contents (otherwise multiprocessing tries to use pickle)
  """

  def __init__(self, x):
    self.x = x

  def __getstate__(self):
    return cpk.dumps(self.x)

  def __setstate__(self, ob):
    self.x = pk.loads(ob)
