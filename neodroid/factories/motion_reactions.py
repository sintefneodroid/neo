#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from neodroid.utilities.unity_specifications.motion import Motion
from neodroid.utilities.unity_specifications import Reaction
from neodroid.utilities.unity_specifications.reaction_parameters import ReactionParameters

__author__ = 'Christian Heider Nielsen'

import numpy


def verify_motion_reactions(*,
                            input_reactions,
                            environment_descriptions
                            #: Mapping[str, EnvironmentDescription]
                            ):
  outs = []
  if environment_descriptions:
    if len(input_reactions) is not len(environment_descriptions):
      logging.warning(
        f'Inputs({len(input_reactions)}) and'
        f' environment descriptions({len(environment_descriptions)}) are not the '
        f'same length')

    for input, (env_name, env_desc) in zip(input_reactions,
                                           environment_descriptions.items()):
      actors = env_desc.actors.values()
      if actors:
        if isinstance(input, Reaction):
          is_valid_motions = all(isinstance(m, Motion) for m in input.motions)
          if is_valid_motions:
            return input
          else:
            input.motions = construct_motions_from_list(input.motions,
                                                        actors
                                                        )
            return input
        elif isinstance(input, list):
          is_valid_motions = all(isinstance(m, Motion) for m in input)
          if is_valid_motions:
            parameters = ReactionParameters(terminable=True,
                                            step=True,
                                            reset=False,
                                            configure=False,
                                            describe=False,
                                            episode_count=True)
            outs.append(Reaction(parameters=parameters,
                                 configurations=[],
                                 motions=input, environment_name=env_name))
          else:
            outs.append(construct_individual_reactions_from_list(input, actors, env_name=env_name))
        elif isinstance(input, (int, float)):
          outs.append(construct_individual_reactions_from_list([input], actors, env_name=env_name))
        elif isinstance(input, (numpy.ndarray, numpy.generic)):
          a = construct_individual_reactions_from_list(input.astype(float).tolist(),
                                                       actors,
                                                       env_name=env_name)
          outs.append(a)
  else:
    parameters = ReactionParameters(describe=True)
    outs.append(Reaction(parameters=parameters, environment_name='all'))
  return outs


def construct_individual_reactions_from_list(motion_list, actors, env_name='all'):
  motions = construct_motions_from_list(motion_list, actors)
  parameters = ReactionParameters(terminable=True, step=True, reset=False, configure=False,
                                  describe=False, episode_count=True)
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
