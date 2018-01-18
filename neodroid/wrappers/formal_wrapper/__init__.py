from .formal_wrapper import NeodroidFormalWrapper
import numpy as np


def make(environment, **kwargs):
  return NeodroidFormalWrapper(name=environment, **kwargs)

def seed(seed):
  np.random.random(seed)