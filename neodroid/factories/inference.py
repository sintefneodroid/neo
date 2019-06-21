#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.factories import construct_step_reaction, verify_configuration_reaction

__author__ = 'cnheider'
__doc__ = ''

def maybe_infer_motion_reaction(*,
                                input_reactions,
                                normalise,
                                description):
  '''

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
    out_reaction = construct_step_reaction(input_reactions,
                                           description,
                                           normalise,
                                           )
  else:
    out_reaction = construct_step_reaction(input_reactions,
                                           None,
                                           False
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