from .ale_wrapper import NeodroidALEWrapper


def make(environment, configuration=None):
  return NeodroidALEWrapper(name=environment)
