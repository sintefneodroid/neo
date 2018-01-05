from io import BytesIO

import flatbuffers as flb
import numpy as np

from neodroid import modeling as N
from neodroid.messaging import FBSModels as F


def build_reaction(input_reaction):
  B = flb.Builder(0)

  unobservables = build_unobservables(B,input_reaction)

  configurations = build_configurations(B, input_reaction)
  motions = build_motions(B, input_reaction)

  environment_string_offset = B.CreateString('all')

  F.FBSReactionStart(B)
  F.FBSReactionAddParameters(B,
                             F.CreateFBSReactionParameters(B,
                                                           input_reaction.get_parameters().get_terminable(),
                                                           input_reaction.get_parameters().get_step(),
                                                           input_reaction.get_parameters().get_reset(),
                                                           input_reaction.get_parameters().get_configure(),
                                                           input_reaction.get_parameters().get_describe()))
  F.FBSReactionAddEnvironmentName(B, environment_string_offset)
  F.FBSReactionAddMotions(B, motions)
  F.FBSReactionAddConfigurations(B, configurations)
  F.FBSReactionAddUnobservables(B, unobservables)

  flat_reaction = F.FBSReactionEnd(B)
  B.Finish(flat_reaction)

  return B.Output()

def build_unobservables(B,
                        input_reaction,
                        bodies=None,
                        poses=None):
  F.FBSUnobservablesStart(B)
  if bodies:
    F.FBSUnobservablesAddPoses(B, poses)
  if poses:
    F.FBSUnobservablesAddBodies(B, bodies)
  return F.FBSUnobservablesEnd(B)

def build_poses(B, input_reaction, state):
  pl = state.PosesLength()
  F.FBSUnobservablesStartPosesVector(B, pl)
  for i in range(pl):
    pose = state.Poses(i)
    pos = pose.Position(F.FBSVector3())
    rot = pose.Rotation(F.FBSQuaternion())
    F.CreateFBSQuaternionTransform(B, pos.X(), pos.Y(), pos.Z(), rot.X(), rot.Y(), rot.Z(), rot.W())
  return B.EndVector(pl)


def build_bodies(B, input_reaction, state):
  bl = state.BodiesLength()
  F.FBSUnobservablesStartBodiesVector(B, bl)
  for i in range(bl):
    body = state.Bodies(i)
    vel = body.Velocity(F.FBSVector3())
    ang = body.AngularVelocity(F.FBSVector3())
    F.CreateFBSBody(B, vel.X(), vel.Y(), vel.Z(), ang.X(), ang.Y(), ang.Z())
  return B.EndVector(bl)


def build_motions(B, input_reaction):
  motion_offsets = []
  for input_motion in input_reaction.get_motions():
    actor_string_offset = B.CreateString(
        input_motion.get_actor_name())
    motor_string_offset = B.CreateString(
        input_motion.get_motor_name())
    F.FBSMotionStart(B)
    F.FBSMotionAddActorName(B, actor_string_offset)
    F.FBSMotionAddMotorName(B, motor_string_offset)
    F.FBSMotionAddStrength(B, input_motion.get_strength())
    motion_offset = F.FBSMotionEnd(B)
    motion_offsets.append(motion_offset)

  F.FBSReactionStartMotionsVector(B, len(motion_offsets))
  for input_motion in motion_offsets:
    B.PrependUOffsetTRelative(input_motion)
  return B.EndVector(len(motion_offsets))


def build_configurations(B, input_reaction):
  configurations_offsets = []
  for input_configuration in input_reaction.get_configurations():
    name_string_offset = B.CreateString(
        input_configuration.get_configurable_name())
    F.FBSConfigurationStart(B)
    F.FBSConfigurationAddConfigurableName(B, name_string_offset)
    F.FBSConfigurationAddConfigurableValue(B, input_configuration.get_configurable_value())
    configuration_offset = F.FBSConfigurationEnd(B)
    configurations_offsets.append(configuration_offset)

  F.FBSReactionStartConfigurationsVector(B, len(configurations_offsets))
  for input_configuration in configurations_offsets:
    B.PrependUOffsetTRelative(input_configuration)
  return B.EndVector(len(configurations_offsets))


def deserialize_state(state):
  s = F.FBSState.GetRootAsFBSState(state, 0)
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
      actors[actor.get_name()] = actor
  return actors


def create_observers(flat_state):
  observers = {}

  for i in range(flat_state.ObserversLength()):
    flat_observer = flat_state.Observers(i)
    if flat_observer.ObservationType() is F.FBSObserverData.FBSEulerTransform:
      observers[flat_observer.ObserverName()] = create_euler_transform(flat_observer)
    elif flat_observer.ObservationType() is F.FBSObserverData.FBSBodyObservation:
      observers[flat_observer.ObserverName()] = create_body(flat_observer)
    elif flat_observer.ObservationType() is F.FBSObserverData.FBSByteArray:
      observers[flat_observer.ObserverName()] = create_data(flat_observer)
  return observers


def create_poses(flat_state):
  poses = np.zeros((flat_state.PosesLength(), 7))
  for i in range(flat_state.PosesLength()):
    pose = flat_state.Poses(i)
    pos = pose.Position(F.FBSVector3())
    rot = pose.Rotation(F.FBSQuaternion())
    poses[i] = [pos.X(), pos.Y(), pos.Z(), rot.X(), rot.Y(), rot.Z(), rot.W()]
  return poses


def create_bodies(flat_state):
  bodies = np.zeros((flat_state.PosesLength(), 6))
  for i in range(flat_state.BodiesLength()):
    body = flat_state.Bodies(i)
    vel = body.Velocity(F.FBSVector3())
    ang = body.AngularVelocity(F.FBSVector3())
    bodies[i] = [vel.X(), vel.Y(), vel.Z(), ang.X(), ang.Y(), ang.Z()]
  return bodies


def create_euler_transform(flat_observer):
  transform = F.FBSEulerTransform()
  transform.Init(flat_observer.Observation().Bytes, flat_observer.Observation().Pos)
  position = transform.Position()
  rotation = transform.Rotation()
  direction = transform.Direction()
  data = [[position.X(), position.Y(), position.Z()],
          [rotation.X(), rotation.Y(), rotation.Z()],
          [direction.X(), direction.Y(), direction.Z()]]
  input_observer = N.Observer(
      flat_observer.ObserverName(),
      data
  )
  return input_observer


def create_body(flat_observer):
  body = F.FBSBody()
  body.Init(flat_observer.Data().Bytes, flat_observer.Data().Pos)
  velocity = body.Velocity(F.FBSVector3())
  angular_velocity = body.AngularVelocity(F.FBSVector3())
  data = [[velocity.X(), velocity.Y(), velocity.Z()],
          [angular_velocity.X(), angular_velocity.Y(),
           angular_velocity.Z()]]
  input_observer = N.Observer(
      flat_observer.ObserverName(),
      data
  )
  return input_observer


def create_position(fbs_configurable):
  pos = F.FBSPosition()
  pos.Init(fbs_configurable.CurrentValue().Bytes, fbs_configurable.CurrentValue().Pos)
  position = pos.Position()
  data = [position.X(), position.Y(), position.Z()]
  return data


def create_configurables(flat_environment_description):
  configurables = {}
  if flat_environment_description:
    for i in range(flat_environment_description.ConfigurablesLength()):
      fbs_configurable = flat_environment_description.Configurables(i)
      current_value = None

      if fbs_configurable.CurrentValueType() is F.FBSObserverData.FBSPosition:
        current_value = create_position(fbs_configurable)

      configurable = N.Configurable(
          fbs_configurable.ConfigurableName(),
          N.InputRange(fbs_configurable.ValidInput().DecimalGranularity(),
                       fbs_configurable.ValidInput().MinValue(),
                       fbs_configurable.ValidInput().MaxValue()),
          current_value)
      configurables[configurable.get_configurable_name()] = configurable
  return configurables


def create_data(flat_observer):
  byte_array = F.FBSByteArray()
  byte_array.Init(flat_observer.Observation().Bytes, flat_observer.Observation().Pos)
  data = np.array(
      [byte_array.ByteArray(i) for i in range(byte_array.ByteArrayLength())],
      dtype=np.uint8).tobytes()
  # data = byte_array.ByteArrayAsNumpy()
  data = BytesIO(data)
  input_observer = N.Observer(
      flat_observer.ObserverName(),
      data
  )
  return input_observer


def create_motors(flat_actor):
  motors = {}
  for i in range(flat_actor.MotorsLength()):
    flat_motor = flat_actor.Motors(i)
    input_motor = N.Motor(flat_motor.MotorName(),
                          flat_motor.ValidInput(),
                          flat_motor.EnergySpentSinceReset())
    motors[input_motor.get_name()] = input_motor
  return motors


def create_valid_range(flat_range):
  return N.InputRange(flat_range.DecimalGranularity(), flat_range.MinValue(), flat_range.MaxValue())
