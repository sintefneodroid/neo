#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.utilities.exceptions.exceptions import NoUnobservablesException

__author__ = 'cnheider'

import flatbuffers
import numpy as np

from neodroid.messaging import FBSModels as F


def serialise_reactions(input_reactions):
  B = flatbuffers.Builder(1)

  reaction_offsets = []
  for reaction in input_reactions:
    reaction_offsets.append(serialise_reaction(B, reaction))

  l = len(reaction_offsets)
  F.FReactionsStartReactionsVector(B, l)
  for offset in reaction_offsets:
    B.PrependUOffsetTRelative(offset)
  reactions_vector_offset = B.EndVector(l)

  F.FReactionsStart(B)
  F.FReactionsAddReactions(B, reactions_vector_offset)
  # F.FReactionsAddSimulatorConfiguration(B,None)
  # TODO: int should be a string in api version  F.FReactionsAddApiVersion(B, '0.1.0')
  # also use create string before constructing reactions datatype.
  flat_reactions = F.FReactionsEnd(B)

  B.Finish(flat_reactions)
  return B.Output()


def serialise_reaction(B, input_reaction):
  unobservables = serialise_unobservables(B, input_reaction)
  displayables = serialise_displayables(B, input_reaction)
  configurations = serialise_configurations(B, input_reaction)
  motions = serialise_motions(B, input_reaction)

  environment_string_offset = B.CreateString(input_reaction.environment_name)
  serialised_message_string_offset = B.CreateString(input_reaction.serialised_message)

  F.FReactionStart(B)
  F.FReactionAddParameters(B,
                           F.CreateFReactionParameters(B,
                                                       input_reaction.parameters.terminable,
                                                       input_reaction.parameters.step,
                                                       input_reaction.parameters.reset,
                                                       input_reaction.parameters.configure,
                                                       input_reaction.parameters.describe,
                                                       input_reaction.parameters.episode_count
                                                       ),
                           )
  F.FReactionAddEnvironmentName(B, environment_string_offset)
  F.FReactionAddMotions(B, motions)
  F.FReactionAddConfigurations(B, configurations)
  F.FReactionAddDisplayables(B, displayables)
  F.FReactionAddSerialisedMessage(B, serialised_message_string_offset)
  if unobservables is not None:
    F.FReactionAddUnobservables(B, unobservables)

  return F.FReactionEnd(B)


def serialise_unobservables(B, input_reaction):
  unobservables = input_reaction.unobservables
  if unobservables:
    unobservables = unobservables.unobservables
    if not unobservables:
      raise NoUnobservablesException('You probably did not receive any unobservables, check you simulator '
                                     'configuration, maybe you want to always serialise unobservables. If '
                                     'so you need check the corresponding option.')
    poses = serialise_poses(B, unobservables)
    bodies = serialise_bodies(B, unobservables)

    F.FUnobservablesStart(B)
    F.FUnobservablesAddPoses(B, poses)
    F.FUnobservablesAddBodies(B, bodies)
    return F.FUnobservablesEnd(B)


def serialise_poses(B, fu):
  pl = fu.PosesLength()
  F.FUnobservablesStartPosesVector(B, pl)
  for i in range(pl):
    pose = fu.Poses(i)
    pos = pose.Position(F.FVector3())
    rot = pose.Rotation(F.FQuaternion())
    F.CreateFQuaternionTransform(
        B, pos.X(), pos.Y(), pos.Z(), rot.X(), rot.Y(), rot.Z(), rot.W()
        )
  return B.EndVector(pl)


def serialise_bodies(B, fu):
  bl = fu.BodiesLength()
  F.FUnobservablesStartBodiesVector(B, bl)
  for i in range(bl):
    body = fu.Bodies(i)
    vel = body.Velocity(F.FVector3())
    ang = body.AngularVelocity(F.FVector3())
    F.CreateFBody(B, vel.X(), vel.Y(), vel.Z(), ang.X(), ang.Y(), ang.Z())
  return B.EndVector(bl)


def serialise_motions(B, input_reaction):
  motion_offsets = []
  for input_motion in input_reaction.motions:
    actor_string_offset = B.CreateString(input_motion.actor_name)
    motor_string_offset = B.CreateString(input_motion.motor_name)
    F.FMotionStart(B)
    F.FMotionAddActorName(B, actor_string_offset)
    F.FMotionAddMotorName(B, motor_string_offset)
    F.FMotionAddStrength(B, input_motion.strength)
    motion_offset = F.FMotionEnd(B)
    motion_offsets.append(motion_offset)

  l = len(motion_offsets)
  F.FReactionStartMotionsVector(B, l)
  for input_motion in motion_offsets:
    B.PrependUOffsetTRelative(input_motion)
  return B.EndVector(l)


def serialise_displayables(B, input_reaction):
  displayables_offsets = []
  if input_reaction.displayables is not None:
    for input_displayable in input_reaction.displayables:
      name_string_offset = B.CreateString(input_displayable.displayable_name)

      displayable_value_type = F.FDisplayableValue.NONE
      displayable_value_offset = None
      input_value = input_displayable.displayable_value
      if isinstance(input_value, float) or isinstance(input_value, int):
        displayable_value_type = F.FDisplayableValue.FValue
        F.FValueStart(B)
        F.FValueAddVal(B, float(input_value))
        displayable_value_offset = F.FValueEnd(B)
      elif isinstance(input_value, str):
        displayable_value_type = F.FDisplayableValue.FString
        v = B.CreateString(input_value)
        F.FStringStart(B)
        F.FStringAddStr(B, v)
        displayable_value_offset = F.FStringEnd(B)
      elif isinstance(input_value, tuple):
        displayable_value_type = F.FDisplayableValue.FValuedVector3s
        _length = len(input_value[0])

        a0 = input_value[0]
        a1 = input_value[1]

        F.FValuedVector3sStartValsVector(B, _length)
        for v_ in reversed(a0):
          v = np.float64(v_)
          B.PrependFloat64(v)
        values_offset = B.EndVector(_length)

        F.FValuedVector3sStartPointsVector(B, _length)
        for p in reversed(a1):
          x, y, z = np.float64(p)
          F.CreateFVector3(B, x, y, z)
        points = B.EndVector(_length)

        F.FValuedVector3sStart(B)
        F.FValuedVector3sAddVals(B, values_offset)
        F.FValuedVector3sAddPoints(B, points)
        displayable_value_offset = F.FValuedVector3sEnd(B)

      elif isinstance(input_value, list) or isinstance(input_value, np.ndarray) and len(input_value[0]) == 3:
        displayable_value_type = F.FDisplayableValue.FVector3s
        _length = len(input_value)

        F.FVector3sStartPointsVector(B, _length)
        for p in reversed(input_value):
          x, y, z = p
          F.CreateFVector3(B, x, y, z)
        points = B.EndVector(_length)

        F.FVector3sStart(B)
        F.FVector3sAddPoints(B, points)
        displayable_value_offset = F.FVector3sEnd(B)

      elif isinstance(input_value, list) or isinstance(input_value, np.ndarray):
        displayable_value_type = F.FDisplayableValue.FValues
        _length = len(input_value)
        F.FValuesStartValsVector(B, _length)
        for v_ in reversed(input_value):
          B.PrependFloat64(np.float64(v_))
        values_offset = B.EndVector(_length)

        F.FValuesStart(B)
        F.FValuesAddVals(B, values_offset)
        displayable_value_offset = F.FValuesEnd(B)

      F.FDisplayableStart(B)
      F.FDisplayableAddDisplayableName(B, name_string_offset)
      F.FDisplayableAddDisplayableValueType(B, displayable_value_type)
      F.FDisplayableAddDisplayableValue(B, displayable_value_offset)
      displayable_offset = F.FDisplayableEnd(B)
      displayables_offsets.append(displayable_offset)

  F.FReactionStartConfigurationsVector(B, len(displayables_offsets))
  for offset in displayables_offsets:
    B.PrependUOffsetTRelative(offset)
  return B.EndVector(len(displayables_offsets))


def serialise_configurations(B, input_reaction):
  configurations_offsets = []
  if input_reaction.configurations is not None:
    for input_configuration in input_reaction.configurations:
      name_string_offset = B.CreateString(input_configuration.configurable_name)
      F.FConfigurationStart(B)
      F.FConfigurationAddConfigurableName(B, name_string_offset)
      F.FConfigurationAddConfigurableValue(
          B, input_configuration.configurable_value
          )
      configuration_offset = F.FConfigurationEnd(B)
      configurations_offsets.append(configuration_offset)

  F.FReactionStartConfigurationsVector(B, len(configurations_offsets))
  for input_configuration in configurations_offsets:
    B.PrependUOffsetTRelative(input_configuration)
  return B.EndVector(len(configurations_offsets))
