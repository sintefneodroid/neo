"""
.. module:: neodroid
   :platform: Unix, Windows
   :synopsis: An API for communicating with a Unity Game process.

.. moduleauthor:: Christian Heider Nielsen <chrini13@student.aau.dk>


"""

from .neodroid_environment import NeodroidEnvironment
from .models import Configuration
from .models import Reaction
from .models import Motion

def make(environment,configuration=None):
  return NeodroidEnvironment(name=environment)
