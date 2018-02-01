# Copied from https://github.com/ghliu/pytorch-ddpg/blob/master/random_process.py
import numpy as np


# [reference] https://github.com/matthiasplappert/keras-rl/blob/master/rl/random.py

class RandomProcess(object):
  def reset(self):
    raise NotImplementedError

  def sample(self):
    raise NotImplementedError



