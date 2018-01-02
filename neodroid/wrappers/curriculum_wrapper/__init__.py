from .curriculum_wrapper import NeodroidCurriculumWrapper


def make(environment, **kwargs):
  return NeodroidCurriculumWrapper(name=environment, **kwargs)
