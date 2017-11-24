from .gym_wrapper import NeodroidGymWrapper


def make(environment, **kwargs):
  return NeodroidGymWrapper(name=environment, **kwargs)
