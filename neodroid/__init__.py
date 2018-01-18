"""
.. module:: neodroid
   :platform: Unix, Windows
   :synopsis: An API for communicating with a Unity Game process.

.. moduleauthor:: Christian Heider Nielsen <chrini13@student.aau.dk>


"""
import numpy as np
from .neodroid_environment import NeodroidEnvironment

def make(environment, configuration=None):
  return NeodroidEnvironment(name=environment)

def seed(seed):
  np.random.seed(seed)