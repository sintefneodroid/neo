import numpy as np

from neodroid.utilities import Space


class Env(object):

  @property
  def observation_space(self):
    return Space(low=-np.inf, high=np.inf, shape=(2,))


  @property
  def action_space(self):
    return Space(low=-0.1, high=0.1, shape=(2,))