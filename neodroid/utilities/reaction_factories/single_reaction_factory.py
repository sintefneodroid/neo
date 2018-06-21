#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.utilities.unused.debug import print_return

__author__ = 'cnheider'

import numpy as np

from neodroid import models as M


def _norm_action(action, motion_space):
  act_k = (motion_space.max_value - motion_space.min_value) / 2.
  act_b = (motion_space.max_value + motion_space.min_value) / 2.
  return act_k * action + act_b


def _reverse_norm_action(self, action):
  act_k_inv = 2. / (self.action_space.high - self.action_space.low)
  act_b = (self.action_space.high + self.action_space.low) / 2.
  return act_k_inv * (action - act_b)


@print_return
def construct_step_reaction(reaction_input, environment_description, normalise=False, verbose=False):
  """

  :param verbose:
  :param environment_description:
  :param normalise:
  :type reaction_input: object
  """
  if environment_description:
    parameters = M.ReactionParameters(terminable=True, step=True,
                                      episode_count=True)
    actors = environment_description.actors.values()
    if actors:
      if isinstance(reaction_input, M.Reaction):
        is_valid_motions = all(isinstance(m, M.Motion) for m in reaction_input.motions)
        if is_valid_motions:
          return reaction_input
        else:
          reaction_input.motions = construct_motions_from_list(reaction_input.motions, actors, normalise)
          return reaction_input
      elif isinstance(reaction_input, list):
        is_valid_motions = all(isinstance(m, M.Motion) for m in reaction_input)
        if is_valid_motions:

          return M.Reaction(parameters=parameters, motions=reaction_input)
        else:
          return construct_reaction_from_list(reaction_input, actors, normalise)
      elif isinstance(reaction_input, int):
        return construct_reaction_from_list([reaction_input], actors, normalise)
      elif isinstance(reaction_input, float):
        return construct_reaction_from_list([reaction_input], actors, normalise)
      elif isinstance(reaction_input, (np.ndarray, np.generic)):
        a = construct_reaction_from_list(reaction_input.astype(float).tolist(), actors, normalise)
        return a
  if isinstance(reaction_input, M.Reaction):
    return reaction_input
  parameters = M.ReactionParameters(describe=True)
  return M.Reaction(parameters=parameters)


def construct_reaction_from_list(motion_list, actors, normalise):
  motions = construct_motions_from_list(motion_list, actors, normalise)
  parameters = M.ReactionParameters(terminable=True, step=True, episode_count=True)
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
          _norm_action(list_val, actor_motor_tuple[2]),
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


@print_return
def verify_configuration_reaction(*, input_reaction, environment_description, verbose=False):
  if environment_description:
    parameters = M.ReactionParameters(reset=True,
                                      configure=True,
                                      describe=True)
    configurables = environment_description.configurables.values()
    if configurables:
      if isinstance(input_reaction, M.Reaction):
        if input_reaction.configurations:
          is_valid_configurations = all(isinstance(m, M.Configuration) for m in input_reaction.configurations)
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
        is_valid_configurations = all(isinstance(c, M.Configuration) for c in input_reaction)
        if is_valid_configurations:
          return M.Reaction(parameters=parameters, configurations=input_reaction)
        else:
          return construct_configuration_reaction_from_list(input_reaction, configurables)
      elif isinstance(input_reaction, int):
        return construct_configuration_reaction_from_list([input_reaction], configurables)
      elif isinstance(input_reaction, float):
        return construct_configuration_reaction_from_list([input_reaction], configurables)
      elif isinstance(input_reaction, (np.ndarray, np.generic)):
        a = construct_configuration_reaction_from_list(input_reaction.astype(float).tolist(), configurables)
        return a
  if isinstance(input_reaction, M.Reaction):
    return input_reaction
  parameters = M.ReactionParameters(reset=True,
                                    configure=True,
                                    describe=True)
  return M.Reaction(parameters=parameters)


def construct_configuration_reaction_from_list(configuration_list, configurables):
  configurations = construct_configurations_from_known_observables(
      configuration_list, configurables
      )
  parameters = M.ReactionParameters(reset=True, configure=True, describe=True)
  return M.Reaction(parameters=parameters, configurations=configurations)


def construct_configurations_from_known_observables(input_list, configurables):
  new_configurations = [
    M.Configuration(configurable.configurable_name, list_val)
    for (list_val, configurable) in zip(input_list, configurables)
    ]
  return new_configurations