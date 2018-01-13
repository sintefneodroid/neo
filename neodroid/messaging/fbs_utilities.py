from io import BytesIO

import flatbuffers as flb
import numpy as np

from neodroid import models as N
from neodroid.messaging import FBSModels as F


def build_reaction(input_reaction):
  B = flb.Builder(0)

  unobservables = build_unobservables(B, input_reaction)

  configurations = build_configurations(B, input_reaction)
  motions = build_motions(B, input_reaction)

  environment_string_offset = B.CreateString('all')

  F.FReactionStart(B)
  F.FReactionAddParameters(B,
                             F.CreateFReactionParameters(B,
                                                           input_reaction.parameters.terminable,
                                                           input_reaction.parameters.step,
                                                           input_reaction.parameters.reset,
                                                           input_reaction.parameters.configure,
                                                           input_reaction.parameters.describe,
                                                           input_reaction.parameters.episode_count))
  F.FReactionAddEnvironmentName(B, environment_string_offset)
  F.FReactionAddMotions(B, motions)
  F.FReactionAddConfigurations(B, configurations)
  if unobservables is not None:
    F.FReactionAddUnobservables(B, unobservables)

  flat_reaction = F.FReactionEnd(B)
  B.Finish(flat_reaction)

  return B.Output()


def build_unobservables(B,
                        input_reaction):
  unobservables = input_reaction.unobservables
  if unobservables:
    poses = build_poses(B, unobservables)
    bodies = build_bodies(B, unobservables)

    F.FUnobservablesStart(B)
    F.FUnobservablesAddPoses(B, poses)
    F.FUnobservablesAddBodies(B, bodies)
    return F.FUnobservablesEnd(B)


def build_poses(B, unobservables):
  fu = unobservables._unobservables
  pl = fu.PosesLength()
  F.FUnobservablesStartPosesVector(B, pl)
  for i in range(pl):
    pose = fu.Poses(i)
    pos = pose.Position(F.FVector3())
    rot = pose.Rotation(F.FQuaternion())
    F.CreateFQuaternionTransform(B, pos.X(), pos.Y(), pos.Z(), rot.X(), rot.Y(), rot.Z(), rot.W())
  return B.EndVector(pl)


def build_bodies(B, unobservables):
  fu = unobservables._unobservables
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
    actor_string_offset = B.CreateString(
        input_motion.actor_name)
    motor_string_offset = B.CreateString(
        input_motion.motor_name)
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


def build_configurations(B, input_reaction):
  configurations_offsets = []
  for input_configuration in input_reaction.configurations:
    name_string_offset = B.CreateString(
        input_configuration.configurable_name)
    F.FConfigurationStart(B)
    F.FConfigurationAddConfigurableName(B, name_string_offset)
    F.FConfigurationAddConfigurableValue(B, input_configuration.configurable_value)
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
  return actors


def create_quaternion_transform(flat_observer):
  pass


def create_double(flat_observer):
  pass


def create_observers(flat_state):
  observers = {}

  for i in range(flat_state.ObservationsLength()):
    flat_observer = flat_state.Observations(i)
    data=None
    valid_range=None
    if flat_observer.ObservationType() is F.FObservation.FSingle:
      data = create_single(flat_observer)
      valid_range=flat_observer.ValidRange()
    elif flat_observer.ObservationType() is F.FObservation.FDouble:
      data = create_double(flat_observer)
    elif flat_observer.ObservationType() is F.FObservation.FTriple:
      data = create_euler_transform(flat_observer)
    elif flat_observer.ObservationType() is F.FObservation.FQuadruple:
      data = create_euler_transform(flat_observer)
    elif flat_observer.ObservationType() is F.FObservation.FET:
      data = create_euler_transform(flat_observer)
    elif flat_observer.ObservationType() is F.FObservation.FRB:
      data = create_body(flat_observer)
    elif flat_observer.ObservationType() is F.FObservation.FQT:
      data = create_quaternion_transform(flat_observer)
    elif flat_observer.ObservationType() is F.FObservation.FByteArray:
      data = create_data(flat_observer)

    name = flat_observer.ObservationName().decode()
    observers[name] = N.Observation(name,valid_range, data)
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


def create_euler_transform(flat_observer):
  transform = F.FEulerTransform()
  transform.Init(flat_observer.Observation().Bytes, flat_observer.Observation().Pos)
  position = transform.Position(F.FVector3())
  rotation = transform.Rotation(F.FVector3())
  direction = transform.Direction(F.FVector3())
  return [[position.X(), position.Y(), position.Z()],
          [direction.X(), direction.Y(), direction.Z()],
          [rotation.X(), rotation.Y(), rotation.Z()]
          ]


def create_body(flat_observer):
  body = F.FBody()
  body.Init(flat_observer.Observation().Bytes, flat_observer.Observation().Pos)
  velocity = body.Velocity(F.FVector3())
  angular_velocity = body.AngularVelocity(F.FVector3())
  return [[velocity.X(), velocity.Y(), velocity.Z()],
          [angular_velocity.X(), angular_velocity.Y(),
           angular_velocity.Z()]]


def create_triple(fbs_configurable):
  pos = F.FTriple()
  pos.Init(fbs_configurable.Observation().Bytes, fbs_configurable.Observation().Pos)
  position = pos.Vec3()
  data = [position.X(), position.Y(), position.Z()]
  return data

def create_single(fbs_configurable):
  val = F.FSingle()
  val.Init(fbs_configurable.Observation().Bytes, fbs_configurable.Observation().Pos)
  return val.Value()

def create_configurables(flat_environment_description):
  configurables = {}
  if flat_environment_description:
    for i in range(flat_environment_description.ConfigurablesLength()):
      fbs_configurable = flat_environment_description.Configurables(i)
      observation = None

      if fbs_configurable.ObservationType() is F.FObservation.FTriple:
        observation = create_triple(fbs_configurable)
      elif fbs_configurable.ObservationType() is F.FObservation.FSingle:
        observation = create_single(fbs_configurable)
      elif fbs_configurable.ObservationType() is F.FObservation.FET:
        observation = create_euler_transform(fbs_configurable)

      configurable = N.Configurable(
          fbs_configurable.ConfigurableName().decode(),
          observation)
      configurables[configurable.configurable_name] = configurable
  return configurables


def create_data(flat_observer):
  byte_array = F.FByteArray()
  byte_array.Init(flat_observer.Observation().Bytes, flat_observer.Observation().Pos)
  #data = np.array(
  #    [byte_array.Bytes(i) for i in range(byte_array.BytesLength())],
  #    dtype=np.uint8).tobytes()
  data = byte_array.BytesAsNumpy()
  data = BytesIO(data)
  input_observer = N.Observation(
      flat_observer.ObserverName().decode(),
      data
  )
  return input_observer


def create_motors(flat_actor):
  motors = {}
  for i in range(flat_actor.MotorsLength()):
    flat_motor = flat_actor.Motors(i)
    input_motor = N.Motor(flat_motor.MotorName().decode(),
                          flat_motor.ValidInput(),
                          flat_motor.EnergySpentSinceReset())
    motors[input_motor.motor_name] = input_motor
  return motors


def create_valid_range(flat_range):
  return N.InputRange(flat_range.DecimalGranularity(), flat_range.MinValue(), flat_range.MaxValue())
