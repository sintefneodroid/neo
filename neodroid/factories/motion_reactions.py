# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from typing import Mapping

from neodroid.utilities import EnvironmentDescription, EnvironmentSnapshot
from neodroid.utilities.unity_specifications.motion import Motion
from neodroid.utilities.unity_specifications import Reaction
from neodroid.utilities.unity_specifications.reaction_parameters import (
    ReactionParameters,
)

__author__ = "Christian Heider Nielsen"

import numpy


def verify_motion_reactions(
    *,
    input_reactions,
    environment_descriptions: Mapping[str, EnvironmentDescription],
    environment_snapshots: Mapping[str, EnvironmentSnapshot],
    _auto_reset=False,
):
    outs = []
    if (
        input_reactions is not None
        and environment_descriptions is not None
        and environment_snapshots is not None
        and isinstance(environment_descriptions, Mapping)
        and isinstance(environment_snapshots, Mapping)
        and len(environment_descriptions) > 0
        and len(environment_snapshots) > 0
    ):
        if len(input_reactions) is not len(environment_descriptions):
            logging.warning(
                f"Inputs({len(input_reactions)}) and"
                f" environment descriptions({len(environment_descriptions)}) are not the "
                f"same length"
            )

        for input_a, (env_name, env_desc), (env_name1, env_snap) in zip(
            input_reactions,
            environment_descriptions.items(),
            environment_snapshots.items(),
        ):
            reset = False
            if env_snap.terminated:
                reset = _auto_reset
            actors = env_desc.actors.values()
            if actors:
                if isinstance(input_a, Reaction):
                    is_valid_motions = all(
                        isinstance(m, Motion) for m in input_a.motions
                    )
                    if is_valid_motions:
                        return input_a
                    else:
                        input_a.motions = construct_motions_from_list(
                            input_a.motions, actors
                        )
                        return input_a
                elif isinstance(input_a, list):
                    is_valid_motions = all(isinstance(m, Motion) for m in input_a)
                    if is_valid_motions:
                        parameters = ReactionParameters(
                            terminable=True,
                            step=not reset,
                            reset=reset,
                            configure=False,
                            describe=False,
                            episode_count=not reset,
                        )
                        outs.append(
                            Reaction(
                                parameters=parameters,
                                configurations=[],
                                motions=input_a,
                                environment_name=env_name,
                            )
                        )
                    else:
                        outs.append(
                            construct_individual_reactions_from_list(
                                input_a, actors, env_name=env_name, reset=reset
                            )
                        )
                elif isinstance(input_a, (int, float)):
                    outs.append(
                        construct_individual_reactions_from_list(
                            [input_a], actors, env_name=env_name, reset=reset
                        )
                    )
                elif isinstance(input_a, (numpy.ndarray, numpy.generic)):
                    a = construct_individual_reactions_from_list(
                        input_a.astype(float).tolist(),
                        actors,
                        env_name=env_name,
                        reset=reset,
                    )
                    outs.append(a)
    else:
        parameters = ReactionParameters(describe=True)
        outs.append(Reaction(parameters=parameters, environment_name="all"))
    return outs


def construct_individual_reactions_from_list(
    motion_list, actors, env_name, reset=False
):
    motions = construct_motions_from_list(motion_list, actors)
    parameters = ReactionParameters(
        terminable=True,
        step=not reset,
        reset=reset,
        configure=False,
        describe=False,
        episode_count=not reset,
    )
    return Reaction(motions=motions, parameters=parameters, environment_name=env_name)


def construct_motions_from_list(input_list, actors):
    actor_motor_tuples = [
        (actor.actor_name, motor.actuator_name, motor.motion_space)
        for actor in actors
        for motor in actor.actuators.values()
    ]

    new_motions = [
        Motion(actor_motor_tuple[0], actor_motor_tuple[1], list_val)
        for (list_val, actor_motor_tuple) in zip(input_list, actor_motor_tuples)
    ]
    return new_motions
