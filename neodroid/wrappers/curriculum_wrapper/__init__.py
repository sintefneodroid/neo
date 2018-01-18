from .curriculum_wrapper import NeodroidCurriculumWrapper
import numpy as np

def make(environment, **kwargs):
  return NeodroidCurriculumWrapper(name=environment, **kwargs)

def seed(seed):
  np.random.random(seed)