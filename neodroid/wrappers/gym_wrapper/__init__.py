from .gym_wrapper import NeodroidGymWrapper

def make(environment,configuration=None):
  return NeodroidGymWrapper(name=environment)
