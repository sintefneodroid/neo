#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from typing import Mapping

from neodroid.utilities.transformations.action_transformations import normalise_action

__author__ = 'cnheider'

import numpy as np

from neodroid.interfaces import specifications as M, EnvironmentDescription, ActionSpace


def maybe_infer_multi_motion_reaction(*,
                                      input_reactions,
                                      normalise: bool,
                                      descriptions: Mapping[str, EnvironmentDescription],
                                      action_space: Mapping[str, ActionSpace]):
  '''

  :param action_space:
:param verbose:
:type verbose:
:param input_reactions:
:type input_reactions:
:param normalise:
:type normalise:
:param descriptions:
:type descriptions:
:return:
:rtype:
'''
  if descriptions:
    out_reaction = verify_motion_reactions(reaction_input=input_reactions,
                                           environment_descriptions=descriptions,
                                           normalise=normalise
                                           )
  else:
    out_reaction = verify_motion_reactions(reaction_input=input_reactions,
                                           environment_descriptions=None,
                                           normalise=False
                                           )

  return out_reaction


def maybe_infer_multi_configuration_reaction(input_reactions,
                                             description: Mapping[str, EnvironmentDescription]):
  if description:
    input_reactions = verify_configuration_reactions(input_reaction=input_reactions,
                                                     environment_descriptions=description
                                                     )
  else:
    input_reactions = verify_configuration_reactions(input_reaction=input_reactions,
                                                     environment_descriptions=description)

  return input_reactions


def verify_motion_reactions(*,
                            reaction_input,
                            environment_descriptions: Mapping[str, EnvironmentDescription],
                            normalise: bool = False):
  outs = []
  if environment_descriptions:
    if len(reaction_input) is not len(environment_descriptions):
      logging.warning(
          f'Inputs({len(reaction_input)}) and'
          f' environment descriptions({len(environment_descriptions)}) are not the '
          f'same length')

    for input, (env_name,env_desc) in zip(reaction_input,
                               environment_descriptions.items()):
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
            outs.append(M.Reaction(parameters=parameters,
                                   configurations=[],
                                   motions=input,environment_name=env_name))
          else:
            outs.append(construct_individual_reactions_from_list(input, actors, normalise,env_name=env_name))
        elif isinstance(input, (int, float)):
          outs.append(construct_individual_reactions_from_list([input], actors, normalise,env_name=env_name))
        elif isinstance(input, (np.ndarray, np.generic)):
          a = construct_individual_reactions_from_list(input.astype(float).tolist(),
                                                       actors,
                                                       normalise,env_name=env_name)
          outs.append(a)
    else:
      parameters = M.ReactionParameters(describe=True)
      outs.append( M.Reaction(parameters=parameters))
  return outs


def construct_individual_reactions_from_list(motion_list, actors, normalise,env_name='all'):
  motions = construct_motions_from_list(motion_list, actors, normalise)
  parameters = M.ReactionParameters(terminable=True, step=True, reset=False, configure=False,
                                    describe=False, episode_count=True)
  return M.Reaction(motions=motions, parameters=parameters,environment_name=env_name)


def construct_motions_from_list(input_list, actors, normalise):
  actor_motor_tuples = [
      (actor.actor_name, motor.actuator_name, motor.motion_space)
      for actor in actors
      for motor in actor.actuators.values()
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


def verify_configuration_reactions(input_reaction,
                                   environment_descriptions: Mapping[str, EnvironmentDescription]):
  parameters = M.ReactionParameters(terminable=False,
                                    step=False,
                                    reset=True,
                                    configure=True,
                                    describe=True,
                                    episode_count=False)
  if environment_descriptions:
    configurables = next(iter(environment_descriptions.items()))[1].configurables.values()
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


def construct_configuration_reaction_from_list(configuration_list,
                                               configurables):
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
