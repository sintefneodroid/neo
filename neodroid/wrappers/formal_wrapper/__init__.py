from .formal_wrapper import NeodroidFormalWrapper

def make(environment,configuration=None):
  return NeodroidFormalWrapper(name=environment)
