import numpy as np

from neodroid import Configuration
from neodroid.modeling import Reaction, Motion
from neodroid.modeling.reaction_parameters import ReactionParameters


def verify_motion_reaction(input, environment_description):
  parameters = ReactionParameters(True,True, False, False, False)
  if environment_description:
    actors = environment_description.get_actors().values()
    if actors:
      if isinstance(input, Reaction):
        is_valid_motions = all(isinstance(m, Motion) for m in
                               input.get_motions())
        if is_valid_motions:
          return input
        else:
          input.set_motions(construct_motions_from_list(
              input.get_motions(), actors))
          return input
      elif isinstance(input, list):
        is_valid_motions = all(isinstance(m, Motion) for m in
                               input)
        if is_valid_motions:

          return Reaction(parameters, [], input)
        else:
          return construct_reaction_from_list(input, actors)
      elif isinstance(input, int):
        return construct_reaction_from_list([input], actors)
      elif isinstance(input, float):
        return construct_reaction_from_list([input], actors)
      elif isinstance(input, (np.ndarray, np.generic)):
        a = construct_reaction_from_list(input.astype(float).tolist(), actors)
        return a
  if isinstance(input, Reaction):
    return input
  return Reaction(parameters)


def construct_reaction_from_list(motion_list, actors):
  motions = construct_motions_from_list(motion_list, actors)
  parameters = ReactionParameters(True, True, False, False, False)
  return Reaction(parameters, [], motions)


def construct_motions_from_list(input_list, actors):
  actor_motor_tuples = [(actor.get_name(), motor.get_name())
                        for actor in actors
                        for motor in actor.get_motors().values()]
  new_motions = [Motion(actor_motor_tuple[0], actor_motor_tuple[1], list_val)
                 for (list_val, actor_motor_tuple) in
                 zip(input_list, actor_motor_tuples)]
  return new_motions


def verify_configuration_reaction(input, environment_description):
  parameters = ReactionParameters(False, False, True, True, True,False)
  if environment_description:
    configurables = environment_description.get_configurables().values()
    if configurables:
      if isinstance(input, Reaction):
        is_valid_configurations = all(isinstance(m, Configuration) for m in
                                      input.get_configurations())
        if is_valid_configurations:
          return input
        else:
          input.set_motions(construct_configurations_from_known_observables(
              input.get_configurations(), configurables))
          return input
      elif isinstance(input, list):
        is_valid_configurations = all(isinstance(c, Configuration) for c in
                                      input)
        if is_valid_configurations:

          return Reaction(parameters, input, [])
        else:
          return construct_configuration_reaction_from_list(input, configurables)
      elif isinstance(input, int):
        return construct_configuration_reaction_from_list([input], configurables)
      elif isinstance(input, float):
        return construct_configuration_reaction_from_list([input], configurables)
      elif isinstance(input, (np.ndarray, np.generic)):
        a = construct_configuration_reaction_from_list(input.astype(float).tolist(), configurables)
        return a
  if isinstance(input, Reaction):
    return input
  return Reaction(parameters)


def construct_configuration_reaction_from_list(configuration_list, configurables):
  configurations = construct_configurations_from_known_observables(configuration_list, configurables)
  parameters = ReactionParameters(False, False, True, True, True,False)
  return Reaction(parameters, configurations, [])


def construct_configurations_from_known_observables(input_list, configurables):
  new_configurations = [Configuration(configurable.get_configurable_name(), list_val)
                        for (list_val, configurable) in
                        zip(input_list, configurables)]
  return new_configurations
