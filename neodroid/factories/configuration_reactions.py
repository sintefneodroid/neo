#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import numpy

from neodroid.utilities.unity_specifications import (
    Reaction,
    ReactionParameters,
    Configuration,
    # Motion,
    # EnvironmentDescription,
    Motion,
)

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 9/4/19
           """


def verify_configuration_reactions(
    *,
    input_reactions,
    environment_descriptions
    #: Mapping[str, EnvironmentDescription]
):
    """

:param input_reactions:
:param environment_descriptions:
:return:
"""

    """
if environment_descriptions:
configurables = next(iter(environment_descriptions.items()))[1].configurables.values()
if configurables:
  if isinstance(reaction_input, Reaction):
    if reaction_input.configurations:
      is_valid_configurations = all(
          isinstance(m, Configuration)
          for m in reaction_input.configurations
          )
      if is_valid_configurations:
        return reaction_input
      else:
        reaction_input.motions(
            construct_configurations_from_known_observables(
                reaction_input.configurations, configurables
                )
            )
      return reaction_input
  elif isinstance(reaction_input, list):
    is_valid_configurations = all(
        isinstance(c, Configuration) for c in reaction_input
        )
    if is_valid_configurations:
      return Reaction(
          parameters=parameters, configurations=reaction_input, motions=[]
          )
    else:
      return construct_configuration_reaction_from_list(
          reaction_input, configurables
          )
  elif isinstance(reaction_input, int):
    return construct_configuration_reaction_from_list(
        [reaction_input], configurables
        )
  elif isinstance(reaction_input, float):
    return construct_configuration_reaction_from_list(
        [reaction_input], configurables
        )
  elif isinstance(reaction_input, (numpy.ndarray, numpy.generic)):
    a = construct_configuration_reaction_from_list(
        reaction_input.astype(float).tolist(), configurables
        )
    return a
if isinstance(reaction_input, Reaction):
return reaction_input
return Reaction(parameters=parameters)
"""

    if isinstance(input_reactions, Reaction):
        return input_reactions
    parameters = ReactionParameters(
        terminable=False,
        step=False,
        reset=True,
        configure=True,
        describe=True,
        episode_count=False,
    )
    outs = []
    if environment_descriptions and input_reactions:
        if len(input_reactions) is not len(environment_descriptions):
            logging.warning(
                f"Inputs({len(input_reactions)}) and"
                f" environment descriptions({len(environment_descriptions)}) are not the "
                f"same length"
            )

        for input, (env_name, env_desc) in zip(
            input_reactions, environment_descriptions.items()
        ):
            configurables = env_desc.configurables.values()
            if configurables:
                if isinstance(input, Reaction):
                    is_valid_motions = all(isinstance(m, Motion) for m in input.motions)
                    if is_valid_motions:
                        return input
                    else:
                        input.motions = construct_configuration_reaction_from_list(
                            input.motions, configurables
                        )
                        return input
                elif isinstance(input, list):
                    is_valid_motions = all(isinstance(m, Motion) for m in input)
                    if is_valid_motions:
                        outs.append(
                            Reaction(
                                parameters=parameters,
                                configurations=[],
                                motions=input,
                                environment_name=env_name,
                            )
                        )
                    else:
                        outs.append(
                            construct_configuration_reaction_from_list(
                                input, configurables, env_name=env_name
                            )
                        )
                elif isinstance(input, (int, float)):
                    outs.append(
                        construct_configuration_reaction_from_list(
                            [input], configurables, env_name=env_name
                        )
                    )
                elif isinstance(input, (numpy.ndarray, numpy.generic)):
                    a = construct_configuration_reaction_from_list(
                        input.astype(float).tolist(), configurables, env_name=env_name
                    )
                    outs.append(a)
            else:
                outs.append(Reaction(parameters=parameters, environment_name=env_name))
    else:
        outs.append(Reaction(parameters=parameters, environment_name="all"))
    return outs


def construct_configuration_reaction_from_list(
    configuration_list, configurables, env_name="all"
):
    configurations = construct_configurations_from_known_observables(
        configuration_list, configurables
    )
    parameters = ReactionParameters(
        terminable=False,
        step=False,
        reset=True,
        configure=True,
        describe=True,
        episode_count=False,
    )
    return Reaction(
        parameters=parameters,
        configurations=configurations,
        motions=[],
        environment_name=env_name,
    )


def construct_configurations_from_known_observables(input_list, configurables):
    new_configurations = [
        Configuration(configurable.configurable_name, list_val)
        for (list_val, configurable) in zip(input_list, configurables)
    ]
    return new_configurations
