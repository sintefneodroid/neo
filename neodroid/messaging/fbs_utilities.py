#!/usr/bin/env python3
# coding=utf-8
__author__ = 'cnheider'

from io import BytesIO

import flatbuffers as flb
import numpy as np

from neodroid import models as N
from neodroid.messaging import FBSModels as F


def build_reaction(input_reaction):
  B = flb.Builder(0)

  unobservables = build_unobservables(B, input_reaction)
  displayables = build_displayables(B, input_reaction)
  configurations = build_configurations(B, input_reaction)
  motions = build_motions(B, input_reaction)

  environment_string_offset = B.CreateString(input_reaction.environment_name)
  serialised_message_string_offset = B.CreateString(input_reaction.serialised_message)

  F.FReactionStart(B)
  F.FReactionAddParameters(
      B,
      F.CreateFReactionParameters(
          B,
          input_reaction.parameters.terminable,
          input_reaction.parameters.step,
          input_reaction.parameters.reset,
          input_reaction.parameters.configure,
          input_reaction.parameters.describe,
          input_reaction.parameters.episode_count,
          ),
      )
  F.FReactionAddEnvironmentName(B, environment_string_offset)
  F.FReactionAddMotions(B, motions)
  F.FReactionAddConfigurations(B, configurations)
  F.FReactionAddDisplayables(B, displayables)
  F.FReactionAddSerialisedMessage(B, serialised_message_string_offset)
  if unobservables is not None:
    F.FReactionAddUnobservables(B, unobservables)

  flat_reaction = F.FReactionEnd(B)
  B.Finish(flat_reaction)

  return B.Output()


def build_unobservables(B, input_reaction):
  unobs = input_reaction.unobservables
  if unobs:
    unobs = unobs.unobservables
    poses = build_poses(B, unobs)
    bodies = build_bodies(B, unobs)

    F.FUnobservablesStart(B)
    F.FUnobservablesAddPoses(B, poses)
    F.FUnobservablesAddBodies(B, bodies)
    return F.FUnobservablesEnd(B)


def build_poses(B, fu):
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


def build_bodies(B, fu):
  bl = fu.BodiesLength()
  F.FUnobservablesStartBodiesVector(B, bl)
  for i in range(bl):
    body = fu.Bodies(i)
    vel = body.Velocity(F.FVector3())
    ang = body.AngularVelocity(F.FVector3())
    F.CreateFBody(B, vel.X(), vel.Y(), vel.Z(), ang.X(), ang.Y(), ang.Z())
  return B.EndVector(bl)


def build_motions(B, input_reaction):
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

  F.FReactionStartMotionsVector(B, len(motion_offsets))
  for input_motion in motion_offsets:
    B.PrependUOffsetTRelative(input_motion)
  return B.EndVector(len(motion_offsets))


def build_displayables(B, input_reaction):
  displayables_offsets = []
  if input_reaction.displayables is not None:
    for input_displayable in input_reaction.displayables:
      name_string_offset = B.CreateString(input_displayable.displayable_name)

      displayable_value_type = F.FDisplayableValue.NONE
      displayable_value_offset = None
      input_value = input_displayable.displayable_value
      if type(input_value) is float or type(input_value) is int:
        displayable_value_type = F.FDisplayableValue.FValue
        F.FValueStart(B)
        F.FValueAddVal(B, float(input_value))
        displayable_value_offset = F.FValueEnd(B)
      elif type(input_value) is str:
        displayable_value_type = F.FDisplayableValue.FString
        v = B.CreateString(input_value)
        F.FStringStart(B)
        F.FStringAddStr(B, v)
        displayable_value_offset = F.FStringEnd(B)
      elif type(input_value) is tuple:
        displayable_value_type = F.FDisplayableValue.FValuedVector3s
        _length = len(input_value[0])

        a0 = input_value[0]
        a1 = input_value[1]

        F.FValuedVector3sStartValsVector(B, _length)
        for v_ in reversed(a0):
          v=np.float64(v_)
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

      elif type(input_value) is list or type(input_value) is np.ndarray and len(input_value[0]) == 3:
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

      elif type(input_value) is list or type(input_value) is np.ndarray:
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


def build_configurations(B, input_reaction):
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


def deserialize_state(state):
  s = F.FState.GetRootAsFState(state, 0)
  return s


def create_state(flat_state):
  return N.EnvironmentState(flat_state)


def create_description(flat_description):
  return N.EnvironmentDescription(flat_description)


def create_actors(flat_environment_description):
  actors = {}
  if flat_environment_description:
    for i in range(flat_environment_description.ActorsLength()):
      flat_actor = flat_environment_description.Actors(i)
      actor = N.Actor(flat_actor)
      actors[actor.actor_name] = actor

  out_actors = {}  # All dictionaries in python3.6+ are insertion ordered, actors are sorted by key and
  # inserted so that the order of actor key-value pairs are always the same for all instances the same
  # environment. This is
  # useful when descriptions are used for inference what value (motion strength) in a numeric vector
  # corresponds to what actor.
  for key in sorted(actors.keys()):
    out_actors[key] = actors[key]

  return out_actors


def create_observables(state):
  return [state.Observables(i) for i in range(state.ObservablesLength())]


def create_configurables(flat_environment_description):
  configurables = {}
  if flat_environment_description:
    for i in range(flat_environment_description.ConfigurablesLength()):
      f_conf = flat_environment_description.Configurables(i)
      observation_value, observation_space = unpack_observation(f_conf)

      configurable = N.Configurable(
          f_conf.ConfigurableName().decode(),
          observation_value,
          observation_space
          )
      configurables[configurable.configurable_name] = configurable
  return configurables


def unpack_observation(f_obs):
  value = None
  value_range = None
  if f_obs.ObservationType() is F.FObservation.FSingle:
    value, value_range = create_single(f_obs)
  elif f_obs.ObservationType() is F.FObservation.FDouble:
    value, value_range = create_double(f_obs)
  elif f_obs.ObservationType() is F.FObservation.FTriple:
    value, value_range = create_triple(f_obs)
  elif f_obs.ObservationType() is F.FObservation.FQuadruple:
    value, *_ = create_quadruple(f_obs)
  elif f_obs.ObservationType() is F.FObservation.FArray:
    value, *_ = create_array(f_obs)
  elif f_obs.ObservationType() is F.FObservation.FET:
    value, *_ = create_euler_transform(f_obs)
  elif f_obs.ObservationType() is F.FObservation.FRB:
    value, *_ = create_body(f_obs)
  elif f_obs.ObservationType() is F.FObservation.FQT:
    value, *_ = create_quaternion_transform(f_obs)
  elif f_obs.ObservationType() is F.FObservation.FByteArray:
    value, *_ = create_data(f_obs)

  return value, value_range


def create_observers(flat_state):
  observers = {}

  for i in range(flat_state.ObservationsLength()):
    f_obs = flat_state.Observations(i)
    observation_value, observation_space = unpack_observation(f_obs)

    name = f_obs.ObservationName().decode()
    observers[name] = N.Observation(name, observation_space, observation_value)
  return observers


def create_unobservables(state):
  return N.Unobservables(state.Unobservables())


def create_poses(unobservables):
  poses = np.zeros((unobservables.PosesLength(), 7))
  for i in range(unobservables.PosesLength()):
    pose = unobservables.Poses(i)
    pos = pose.Position(F.FVector3())
    rot = pose.Rotation(F.FQuaternion())
    poses[i] = [pos.X(), pos.Y(), pos.Z(), rot.X(), rot.Y(), rot.Z(), rot.W()]
  return poses


def create_bodies(unobservables):
  bodies = np.zeros((unobservables.PosesLength(), 6))
  for i in range(unobservables.BodiesLength()):
    body = unobservables.Bodies(i)
    vel = body.Velocity(F.FVector3())
    ang = body.AngularVelocity(F.FVector3())
    bodies[i] = [vel.X(), vel.Y(), vel.Z(), ang.X(), ang.Y(), ang.Z()]
  return bodies


def create_euler_transform(f_obs):
  transform = F.FEulerTransform()
  transform.Init(f_obs.Observation().Bytes, f_obs.Observation().Pos)
  position = transform.Position(F.FVector3())
  rotation = transform.Rotation(F.FVector3())
  direction = transform.Direction(F.FVector3())
  return [
    [position.X(), position.Y(), position.Z()],
    [direction.X(), direction.Y(), direction.Z()],
    [rotation.X(), rotation.Y(), rotation.Z()],
    ]


def create_body(f_obs):
  body = F.FBody()
  body.Init(f_obs.Observation().Bytes, f_obs.Observation().Pos)
  velocity = body.Velocity(F.FVector3())
  angular_velocity = body.AngularVelocity(F.FVector3())
  return [
    [velocity.X(), velocity.Y(), velocity.Z()],
    [angular_velocity.X(), angular_velocity.Y(), angular_velocity.Z()],
    ]


def create_quadruple(f_obs):
  q = F.FQuadruple()
  q.Init(f_obs.Observation().Bytes, f_obs.Observation().Pos)
  quad = q.Quat()
  data = [quad.X(), quad.Y(), quad.Z(), quad.W()]
  return data


def create_triple(f_obs):
  pos = F.FTriple()
  pos.Init(f_obs.Observation().Bytes, f_obs.Observation().Pos)
  position = pos.Vec3()
  value = [position.X(), position.Y(), position.Z()]
  value_range = [pos.XRange(), pos.YRange(), pos.ZRange()]
  return value, value_range


def create_double(f_obs):
  pos = F.FDouble()
  pos.Init(f_obs.Observation().Bytes, f_obs.Observation().Pos)
  position = pos.Vec2()
  value = [position.X(), position.Y()]
  value_range = [pos.XRange(), pos.YRange()]
  return value, value_range


def create_single(f_obs):
  val = F.FSingle()
  val.Init(f_obs.Observation().Bytes, f_obs.Observation().Pos)
  value, value_range = val.Value(), val.Range()
  return value, value_range


def create_quaternion_transform(f_obs):
  qt = F.FQT()
  qt.Init(f_obs.Observation().Bytes, f_obs.Observation().Pos)
  position = qt.Transform().Position(F.FVector3())
  rotation = qt.Transform().Rotation(F.FQuaternion())
  data = [
    position.X(),
    position.Y(),
    position.Z(),
    rotation.X(),
    rotation.Y(),
    rotation.Z(),
    rotation.W(),
    ]
  return data


def create_data(f_obs):
  byte_array = F.FByteArray()
  byte_array.Init(f_obs.Observation().Bytes, f_obs.Observation().Pos)
  # data = np.array(
  #    [byte_array.Bytes(i) for i in range(byte_array.BytesLength())],
  #    dtype=np.uint8)
  data = byte_array.BytesAsNumpy()
  data = BytesIO(data.tobytes())
  return data


def create_array(f_obs):
  array = F.FArray()
  array.Init(f_obs.Observation().Bytes, f_obs.Observation().Pos)
  # data = np.array([array.Array(i) for i in range(array.ArrayLength())])
  data = array.ArrayAsNumpy()
  return data


def create_motors(flat_actor):
  motors = {}
  for i in range(flat_actor.MotorsLength()):
    flat_motor = flat_actor.Motors(i)
    input_motor = N.Motor(
        flat_motor.MotorName().decode(),
        flat_motor.ValidInput(),
        flat_motor.EnergySpentSinceReset(),
        )
    motors[input_motor.motor_name] = input_motor

  out_motors = {}  # All dictionaries in python3.6+ are insertion ordered, motors are sorted by key and
  # inserted so that the order of motor key-value pairs are always the same for all instances the same
  # environment. This is
  # useful when descriptions are used for inference what value (motion strength) in a numeric vector
  # corresponds to what motor.
  for key in sorted(motors.keys()):
    out_motors[key] = motors[key]

  return motors


def create_space(flat_range):
  space = N.Space(
      flat_range.DecimalGranularity(), flat_range.MinValue(), flat_range.MaxValue()
      )
  return space
