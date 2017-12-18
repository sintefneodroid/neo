from io import BytesIO

import flatbuffers as flb
import numpy as np

from neodroid import modeling as N
from neodroid.messaging import FBSModels as F


def build_flat_reaction(input_reaction):
  B = flb.Builder(0)

  configurations = None
  motions = None

  if  len(input_reaction.get_configurations()) > 0:
    configurations_vector = build_configurations(B, input_reaction)
    F.FBSConfigurationsStart(B)
    F.FBSConfigurationsAddConfigurations(B, configurations_vector)
    configurations = F.FBSConfigurationEnd(B);
  elif len(input_reaction.get_motions()) > 0:
    motions_vector = build_motions(B, input_reaction)
    F.FBSMotionsStart(B)
    F.FBSMotionsAddMotions(B,motions_vector)
    motions = F.FBSMotionsEnd(B)
  environment_string_offset = B.CreateString('all')

  F.FBSReactionStart(B)
  F.FBSReactionAddReset(B, input_reaction.get_reset())
  F.FBSReactionAddEnvironmentName(B, environment_string_offset)

  if configurations:
    F.FBSReactionAddActionType(B, F.FBSAction.FBSConfigurations)
    F.FBSReactionAddAction(B, configurations)
  elif motions:
    F.FBSReactionAddActionType(B, F.FBSAction.FBSMotions)
    F.FBSReactionAddAction(B, motions)

  flat_reaction = F.FBSReactionEnd(B)
  B.Finish(flat_reaction)

  return B.Output()

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

  F.FBSMotionsStartMotionsVector(B, len(motion_offsets))
  for input_motion in motion_offsets:
    B.PrependUOffsetTRelative(input_motion)
  #F.FBSMotionsAddMotions(B,motion_offsets)
  return B.EndVector(len(motion_offsets))

def build_configurations(B, input_reaction):
  configurations_offsets = []
  for input_configuration in input_reaction.get_configurations():
    name_string_offset = B.CreateString(
        input_configuration.get_configurable_name())
    F.FBSConfigurationStart(B)
    F.FBSConfigurationAddConfigurableName(B,
                                          name_string_offset)
    F.FBSConfigurationAddConfigurableValue(B,
                                           input_configuration.get_configurable_value())
    configuration_offset = F.FBSConfigurationEnd(B)
    configurations_offsets.append(configuration_offset)

  F.FBSConfigurationsStartConfigurationsVector(B,
                                               len(configurations_offsets))
  for input_configuration in configurations_offsets:
    B.PrependUOffsetTRelative(input_configuration)
  #F.FBSConfigurationsAddConfigurations(B,configurations_offsets)
  return B.EndVector(len(configurations_offsets))

def deserialize_state(state):
  s = F.FBSState.GetRootAsFBSState(state, 0)
  return s

def create_state(flat_state):
  state = N.EnvironmentState(flat_state)
  return state

def create_description(flat_description):
  if flat_description is not None:
    return N.EnvironmentDescription(flat_description)
  else:
    return None

def create_actors(flat_environment_description):
  actors = {}
  if flat_environment_description:
    for i in range(1, flat_environment_description.ActorsLength() + 1):
      flat_actor = flat_environment_description.Actors(i)
      motors = create_motors(flat_actor)
      input_actor = N.Actor(
          flat_actor.ActorName(),
          motors)
      actors[input_actor.get_name()] = input_actor
  return actors

def create_observers(flat_state):
  observers = {}

  for i in range(1, flat_state.ObserversLength() + 1):
    flat_observer = flat_state.Observers(i)
    if flat_observer.DataType() is F.FBSObserverData.FBSEulerTransform:
      observers[flat_observer.ObserverName()] = create_euler_transform(flat_observer)
    elif flat_observer.DataType() is F.FBSObserverData.FBSBody:
      observers[flat_observer.ObserverName()] = create_body(flat_observer)
  return observers

def create_euler_transform(flat_observer):
  transform = F.FBSEulerTransform()
  transform.Init(flat_observer.Data().Bytes,flat_observer.Data().Pos)
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
  body.Init(flat_observer.Data().Bytes,flat_observer.Data().Pos)
  velocity = body.Velocity()
  angular_velocity = body.AngularVelocity()
  data = [[velocity.X(), velocity.Y(), velocity.Z()],
          [angular_velocity.X(), angular_velocity.Y(),
           angular_velocity.Z()]]
  input_observer = N.Observer(
      flat_observer.ObserverName(),
      data
  )
  return input_observer


def create_configurables(flat_environment_description):
  configurables = {}
  if flat_environment_description:
    for i in range(1, flat_environment_description.ConfigurablesLength() + 1):
      fbs_configurable = flat_environment_description.Configurables(i)
      configurable = N.Configurable(
          fbs_configurable.ConfigurableName(),
          N.InputRange(fbs_configurable.ValidInput().DecimalGranularity(),fbs_configurable.ValidInput().MinValue(),fbs_configurable.ValidInput().MaxValue()),
          fbs_configurable.HasObserver(),
          fbs_configurable.ObserverName())
      configurables[configurable.get_configurable_name()] = configurable
  return configurables


def create_data(flat_observer):
  data = np.array(
      [
        flat_observer.Data(i)
        for i in range(4, flat_observer.DataLength() + 4)  # 4 and +4 Strips
        # non-png related data
      ],
      dtype=np.uint8).tobytes()  # Weird magic sizes
  bytes_stream = BytesIO(data)
  # bytes_stream.seek(0)
  return bytes_stream


def create_motors(flat_actor):
  motors = {}
  for i in range(1, flat_actor.MotorsLength() + 1):
    flat_motor = flat_actor.Motors(i)
    input_motor = N.Motor(flat_motor.MotorName(),
                          flat_motor.ValidInput(),
                          flat_motor.EnergySpentSinceReset())
    motors[input_motor.get_name()] = input_motor
  return motors
