import logging
import numpy as np
import gym

_logger = logging.getLogger(__name__)

class FrameSkippingWrapper(gym.Wrapper):

  def __init__(self, env, skips):
    super().__init__(env)
    self._skips = skips

  def _step(self, action):

    self._state_buffer=[]

    for _ in range(self._skips):

      observation, reward, done, info = self.env.step(action[0, 0])
      next_state = self.env.get_screen()
      self._state_buffer.append(next_state)

      if done:
        break

    return np.array(self._state_buffer)

  def _reset(self):
    return self.env.reset()
