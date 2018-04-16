#!/usr/bin/env python3
# coding=utf-8
__author__ = 'cnheider'

import numpy as np

from neodroid import models as M


def _action(action, motion_space):
  act_k = (motion_space.max_value - motion_space.min_value) / 2.
  act_b = (motion_space.max_value + motion_space.min_value) / 2.
  return act_k * action + act_b


def _reverse_action(self, action):
  act_k_inv = 2. / (self.action_space.high - self.action_space.low)
  act_b = (self.action_space.high + self.action_space.low) / 2.
  return act_k_inv * (action - act_b)


def verify_motion_reaction(input, environment_description, normalise=False):
  parameters = M.ReactionParameters(True, True, False, False, False)
  if environment_description:
    actors = environment_description.actors.values()
    if actors:
      if isinstance(input, M.Reaction):
        is_valid_motions = all(isinstance(m, M.Motion) for m in
                               input.motions)
        if is_valid_motions:
          return input
        else:
          input.motions = construct_motions_from_list(
              input.motions, actors, normalise)
          return input
      elif isinstance(input, list):
        is_valid_motions = all(isinstance(m, M.Motion) for m in
                               input)
        if is_valid_motions:

          return M.Reaction(parameters=parameters, configurations=[], motions=input)
        else:
          return construct_reaction_from_list(input, actors, normalise)
      elif isinstance(input, int):
        return construct_reaction_from_list([input], actors, normalise)
      elif isinstance(input, float):
        return construct_reaction_from_list([input], actors, normalise)
      elif isinstance(input, (np.ndarray, np.generic)):
        a = construct_reaction_from_list(input.astype(float).tolist(), actors, normalise)
        return a
  if isinstance(input, M.Reaction):
    return input
  return M.Reaction(parameters=parameters)


def construct_reaction_from_list(motion_list, actors, normalise):
  motions = construct_motions_from_list(motion_list, actors, normalise)
  parameters = M.ReactionParameters(True, True, False, False, False)
  return M.Reaction(parameters, [], motions)


def construct_motions_from_list(input_list, actors, normalise):
  actor_motor_tuples = [(actor.actor_name, motor.motor_name, motor.motion_space)
                        for actor in actors
                        for motor in actor.motors.values()]
  if normalise:
    new_motions = [
      M.Motion(actor_motor_tuple[0], actor_motor_tuple[1], _action(list_val, actor_motor_tuple[2]))
      for (list_val, actor_motor_tuple) in
      zip(input_list, actor_motor_tuples)]
    return new_motions
  else:
    new_motions = [M.Motion(actor_motor_tuple[0], actor_motor_tuple[1], list_val)
                   for (list_val, actor_motor_tuple) in
                   zip(input_list, actor_motor_tuples)]
    return new_motions


def verify_configuration_reaction(input, environment_description):
  parameters = M.ReactionParameters(False, False, True, True, True, False)
  if environment_description:
    configurables = environment_description.configurables.values()
    if configurables:
      if isinstance(input, M.Reaction):
        if input.configurations:
          is_valid_configurations = all(isinstance(m, M.Configuration) for m in
                                        input.configurations)
          if is_valid_configurations:
            return input
          else:
            input.motions(construct_configurations_from_known_observables(
                input.configurations, configurables))
          return input
      elif isinstance(input, list):
        is_valid_configurations = all(isinstance(c, M.Configuration) for c in
                                      input)
        if is_valid_configurations:
          return M.Reaction(parameters=parameters, configurations=input, motions=[])
        else:
          return construct_configuration_reaction_from_list(input, configurables)
      elif isinstance(input, int):
        return construct_configuration_reaction_from_list([input], configurables)
      elif isinstance(input, float):
        return construct_configuration_reaction_from_list([input], configurables)
      elif isinstance(input, (np.ndarray, np.generic)):
        a = construct_configuration_reaction_from_list(input.astype(float).tolist(), configurables)
        return a
  if isinstance(input, M.Reaction):
    return input
  return M.Reaction(parameters=parameters)


def construct_configuration_reaction_from_list(configuration_list, configurables):
  configurations = construct_configurations_from_known_observables(configuration_list, configurables)
  parameters = M.ReactionParameters(False, False, True, True, True, False)
  return M.Reaction(parameters=parameters, configurations=configurations, motions=[])


def construct_configurations_from_known_observables(input_list, configurables):
  new_configurations = [M.Configuration(configurable.configurable_name, list_val)
                        for (list_val, configurable) in
                        zip(input_list, configurables)]
  return new_configurations
