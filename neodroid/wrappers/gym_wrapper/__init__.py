from .gym_wrapper import NeodroidGymWrapper
import numpy as np

def make(environment, *args, **kwargs):
  return NeodroidGymWrapper(name=environment, *args, **kwargs)


def seed(seed):
  np.random.random(seed)