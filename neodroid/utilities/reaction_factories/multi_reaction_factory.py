#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from neodroid.utilities.debugging_utilities.debug_print_return import print_return_value
from neodroid.utilities.transformations.action_transformations import normalise_action

__author__ = 'cnheider'

import numpy as np
import warnings

from neodroid import models as M


@print_return_value
def verify_motion_reactions(inputs,
                            environment_descriptions,
                            normalise=False,
                            verbose=False):
  if environment_descriptions:
    if len(inputs) is not len(environment_descriptions):
      warnings.warn(
          f'Inputs({len(inputs)}) and environment descriptions({len(environment_descriptions)}) are not the '
          f'same length')
    for input, env_desc in zip(inputs, environment_descriptions):
      actors = env_desc.actors.values()
      if actors:
        if isinstance(input, M.Reaction):
          is_valid_motions = all(isinstance(m, M.Motion) for m in input.motions)
          if is_valid_motions:
            return input
          else:
            input.motions = construct_motions_from_list(input.motions,
                                                        actors,
                                                        normalise)
            return input
        elif isinstance(input, list):
          is_valid_motions = all(isinstance(m, M.Motion) for m in input)
          if is_valid_motions:
            parameters = M.ReactionParameters(terminable=True,
                                              step=True,
                                              reset=False,
                                              configure=False,
                                              describe=False,
                                              episode_count=True)
            return M.Reaction(parameters=parameters,
                              configurations=[],
                              motions=input)
          else:
            return construct_individual_reactions_from_list(input, actors, normalise)
        elif isinstance(input, (int, float)):
          return construct_individual_reactions_from_list([input], actors, normalise)
        elif isinstance(input, (np.ndarray, np.generic)):
          a = construct_individual_reactions_from_list(input.astype(float).tolist(),
                                                       actors,
                                                       normalise)
          return a
  if isinstance(inputs, M.Reaction):
    return inputs
  parameters = M.ReactionParameters(terminable=False,
                                    step=False,
                                    reset=False,
                                    configure=False,
                                    describe=True,
                                    episode_count=False)
  return M.Reaction(parameters=parameters)


def construct_individual_reactions_from_list(motion_list, actors, normalise):
  motions = construct_motions_from_list(motion_list, actors, normalise)
  parameters = M.ReactionParameters(terminable=True, step=True, reset=False, configure=False,
                                    describe=False, episode_count=True)
  return M.Reaction(motions=motions, parameters=parameters)


def construct_motions_from_list(input_list, actors, normalise):
  actor_motor_tuples = [
    (actor.actor_name, motor.motor_name, motor.motion_space)
    for actor in actors
    for motor in actor.motors.values()
    ]
  if normalise:
    new_motions = [
      M.Motion(
          actor_motor_tuple[0],
          actor_motor_tuple[1],
          normalise_action(list_val, actor_motor_tuple[2]),
          )
      for (list_val, actor_motor_tuple) in zip(input_list, actor_motor_tuples)
      ]
    return new_motions
  else:
    new_motions = [
      M.Motion(actor_motor_tuple[0], actor_motor_tuple[1], list_val)
      for (list_val, actor_motor_tuple) in zip(input_list, actor_motor_tuples)
      ]
    return new_motions


@print_return_value
def verify_configuration_reaction(input_reaction,
                                  environment_description,
                                  verbose=False):
  parameters = M.ReactionParameters(terminable=False,
                                    step=False,
                                    reset=True,
                                    configure=True,
                                    describe=True,
                                    episode_count=False)
  if environment_description:
    configurables = environment_description.configurables.values()
    if configurables:
      if isinstance(input_reaction, M.Reaction):
        if input_reaction.configurations:
          is_valid_configurations = all(
              isinstance(m, M.Configuration)
              for m in input_reaction.configurations
              )
          if is_valid_configurations:
            return input_reaction
          else:
            input_reaction.motions(
                construct_configurations_from_known_observables(
                    input_reaction.configurations, configurables
                    )
                )
          return input_reaction
      elif isinstance(input_reaction, list):
        is_valid_configurations = all(
            isinstance(c, M.Configuration) for c in input_reaction
            )
        if is_valid_configurations:
          return M.Reaction(
              parameters=parameters, configurations=input_reaction, motions=[]
              )
        else:
          return construct_configuration_reaction_from_list(
              input_reaction, configurables
              )
      elif isinstance(input_reaction, int):
        return construct_configuration_reaction_from_list(
            [input_reaction], configurables
            )
      elif isinstance(input_reaction, float):
        return construct_configuration_reaction_from_list(
            [input_reaction], configurables
            )
      elif isinstance(input_reaction, (np.ndarray, np.generic)):
        a = construct_configuration_reaction_from_list(
            input_reaction.astype(float).tolist(), configurables
            )
        return a
  if isinstance(input_reaction, M.Reaction):
    return input_reaction
  return M.Reaction(parameters=parameters)


def construct_configuration_reaction_from_list(configuration_list, configurables):
  configurations = construct_configurations_from_known_observables(
      configuration_list, configurables
      )
  parameters = M.ReactionParameters(terminable=False, step=False, reset=True, configure=True,
                                    describe=True, episode_count=False)
  return M.Reaction(parameters=parameters, configurations=configurations, motions=[])


def construct_configurations_from_known_observables(input_list, configurables):
  new_configurations = [
    M.Configuration(configurable.configurable_name, list_val)
    for (list_val, configurable) in zip(input_list, configurables)
    ]
  return new_configurations
