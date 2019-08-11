#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.factories import construct_step_reaction, verify_configuration_reaction
from neodroid.interfaces.spaces import ActionSpace

__author__ = 'cnheider'
__doc__ = ''


def maybe_infer_motion_reaction(*,
                                input_reactions,
                                normalise,
                                description,
                                action_space: ActionSpace):
  '''

  :param action_space:
:param verbose:
:type verbose:
:param input_reactions:
:type input_reactions:
:param normalise:
:type normalise:
:param description:
:type description:
:return:
:rtype:
'''
  if description:
    out_reaction = construct_step_reaction(reaction_input=input_reactions,
                                           environment_description=description,
                                           normalise=normalise,
                                           space=action_space
                                           )
  else:
    out_reaction = construct_step_reaction(reaction_input=input_reactions,
                                           environment_description=None,
                                           normalise=False,
                                           space=action_space
                                           )

  return out_reaction


def maybe_infer_configuration_reaction(input_reaction, description):
  if description:
    input_reaction = verify_configuration_reaction(input_reaction=input_reaction,
                                                   environment_description=description
                                                   )
  else:
    input_reaction = verify_configuration_reaction(input_reaction=input_reaction,
                                                   environment_description=description)

  return input_reaction
