import numpy as np

from .gym_wrapper import NeodroidGymWrapper


def make(environment, *args, **kwargs):
  return NeodroidGymWrapper(name=environment, *args, **kwargs)


def seed(seed):
  np.random.random(seed)
