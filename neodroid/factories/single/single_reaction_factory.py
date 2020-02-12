#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from typing import Sequence

from neodroid.utilities.spaces import ActionSpace
from neodroid.utilities.unity_specifications import (
    EnvironmentDescription,
    Configuration,
    Motion,
    Reaction,
    ReactionParameters,
)
from neodroid.utilities.transformations import normalise_action

__author__ = "Christian Heider Nielsen"

import numpy


# @debug_print_return_value
def verify_motion_reaction(
    *,
    reaction_input,
    action_space: ActionSpace,
    environment_description: EnvironmentDescription = None,
    normalise: bool = False
):
    """

:param action_space:
:param environment_description:
:param normalise:
:type reaction_input: object
"""
    if reaction_input is None:
        logging.info(
            "Received empty reaction, Constructing empty counting terminal step reaction"
        )
        parameters = ReactionParameters(terminable=True, step=True, episode_count=True)
        return Reaction(parameters=parameters)

    if isinstance(reaction_input, Reaction):
        return reaction_input
    if isinstance(reaction_input, list):
        if (
            len(reaction_input) > 0
            and numpy.array([isinstance(ri, Reaction) for ri in reaction_input]).all()
        ):
            return reaction_input

    if isinstance(reaction_input, dict):
        parameters = ReactionParameters(terminable=True, step=True, episode_count=True)
        if isinstance(list(reaction_input.values())[0], dict):
            return Reaction(
                parameters=parameters,
                motions=[
                    Motion(p, k, v)
                    for p, a in reaction_input.items()
                    for k, v in a.items()
                ],
            )

        return Reaction(
            parameters=parameters,
            motions=[Motion("Actor", k, v) for k, v in reaction_input.items()],
        )

    if environment_description:
        parameters = ReactionParameters(terminable=True, step=True, episode_count=True)
        actors = environment_description.actors.values()
        if actors:
            if isinstance(reaction_input, Reaction):
                is_valid_motions = all(
                    isinstance(m, Motion) for m in reaction_input.motions
                )
                if is_valid_motions:
                    return reaction_input
                else:
                    reaction_input.motions = construct_motions_from_list(
                        reaction_input.motions, actors, normalise, action_space
                    )
                    return reaction_input
            elif isinstance(reaction_input, list):
                is_valid_motions = all(isinstance(m, Motion) for m in reaction_input)
                if is_valid_motions:
                    return Reaction(parameters=parameters, motions=reaction_input)
                else:
                    return construct_reaction_from_list(
                        reaction_input, actors, normalise, action_space
                    )
            elif isinstance(reaction_input, (int, float)):
                return construct_reaction_from_list(
                    [reaction_input], actors, normalise, action_space
                )
            elif isinstance(reaction_input, (numpy.ndarray, numpy.generic)):
                a = construct_reaction_from_list(
                    reaction_input.astype(float).tolist(),
                    actors,
                    normalise,
                    action_space,
                )
                return a

    parameters = ReactionParameters(describe=True)
    return Reaction(parameters=parameters)


def construct_reaction_from_list(motion_list, actors, normalise, space):
    if not isinstance(motion_list, list):
        motion_list = [motion_list]
    motions = construct_motions_from_list(motion_list, actors, normalise, space)
    parameters = ReactionParameters(terminable=True, step=True, episode_count=True)
    return Reaction(motions=motions, parameters=parameters)


def construct_motions_from_list(
    input_list, actors, normalise: bool, space: ActionSpace
):
    actor_actuator_tuples = [
        (actor.actor_name, actuator.actuator_name, actuator.motion_space)
        for actor in actors
        for actuator in actor.actuators.values()
    ]
    if isinstance(input_list[0], Sequence):
        if len(input_list) == 1:
            input_list = input_list[0]

    if normalise:
        new_motions = [
            Motion(
                actor_actuator_tuple[0],
                actor_actuator_tuple[1],
                normalise_action(list_val, actor_actuator_tuple[2]),
            )
            for (list_val, actor_actuator_tuple) in zip(
                input_list, actor_actuator_tuples
            )
        ]
        return new_motions
    else:
        new_motions = [
            Motion(actor_actuator_tuple[0], actor_actuator_tuple[1], list_val)
            for (list_val, actor_actuator_tuple) in zip(
                input_list, actor_actuator_tuples
            )
        ]
        return new_motions


# @print_return_value
def verify_configuration_reaction(
    *, input_reaction, environment_description: EnvironmentDescription
):
    if environment_description:
        parameters = ReactionParameters(reset=True, configure=True, describe=True)
        configurables = environment_description.configurables.values()
        if configurables:
            if isinstance(input_reaction, Reaction):
                if input_reaction.configurations:
                    is_valid_configurations = all(
                        isinstance(m, Configuration)
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
                    isinstance(c, Configuration) for c in input_reaction
                )
                if is_valid_configurations:
                    return Reaction(
                        parameters=parameters, configurations=input_reaction
                    )
                else:
                    return construct_configuration_reaction_from_list(
                        input_reaction, configurables
                    )
            elif isinstance(input_reaction, (int, float)):
                return construct_configuration_reaction_from_list(
                    [input_reaction], configurables
                )
            elif isinstance(input_reaction, (numpy.ndarray, numpy.generic)):
                a = construct_configuration_reaction_from_list(
                    input_reaction.astype(float).tolist(), configurables
                )
                return a
    if isinstance(input_reaction, Reaction):
        return input_reaction
    parameters = ReactionParameters(reset=True, configure=True, describe=True)
    return Reaction(parameters=parameters)


def construct_configuration_reaction_from_list(configuration_list, configurables):
    configurations = construct_configurations_from_known_observables(
        configuration_list, configurables
    )
    parameters = ReactionParameters(reset=True, configure=True, describe=True)
    return Reaction(parameters=parameters, configurations=configurations)


def construct_configurations_from_known_observables(input_list, configurables):
    new_configurations = [
        Configuration(configurable.configurable_name, list_val)
        for (list_val, configurable) in zip(input_list, configurables)
    ]
    return new_configurations
