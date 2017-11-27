from .formal_wrapper import NeodroidFormalWrapper


def make(environment,  **kwargs):
  return NeodroidFormalWrapper(name=environment, **kwargs)
