import numpy as np

from neodroid.utilities import Space


class Environment(object):

  def _configure(self):
    raise NotImplementedError

  def _reset(self):
    raise NotImplementedError

  def _react(self):
    raise NotImplementedError

  def _observer(self):
    raise NotImplementedError

  def _display(self):
    raise NotImplementedError

  def _observation_space(self):
    return Space(low=-np.inf, high=np.inf, shape=(2,))

  @property
  def observation_space(self):
    return self._observation_space()

  def _action_space(self):
    return Space(low=-0.1, high=0.1, shape=(2,))

  @property
  def action_space(self):
    return self._action_space()

  def _signal_space(self):
    return -np.inf, np.inf

  @property
  def signal_space(self):
    return self._signal_space()
