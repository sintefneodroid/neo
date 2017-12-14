from io import BytesIO

import flatbuffers as flb
import numpy as np

from neodroid import modeling as neomodels
from neodroid.messaging import FBSModels as flbmodels
from neodroid.messaging.FBSModels import FBSVec3


def build_flat_reaction(input_reaction):
  builder = flb.Builder(0)

  motion_offsets = []
  for input_motion in input_reaction.get_motions():
    actor_string_offset = builder.CreateString(
        input_motion.get_actor_name())
    motor_string_offset = builder.CreateString(
        input_motion.get_motor_name())
    flbmodels.FBSMotionStart(builder)
    flbmodels.FBSMotionAddActorName(builder, actor_string_offset)
    flbmodels.FBSMotionAddMotorName(builder, motor_string_offset)
    flbmodels.FBSMotionAddStrength(builder,
                                   input_motion.get_strength())
    motion_offset = flbmodels.FBSMotionEnd(builder)
    motion_offsets.append(motion_offset)

  flbmodels.FBSReactionStartMotionsVector(builder,
                                          len(motion_offsets))
  for input_motion in motion_offsets:
    builder.PrependUOffsetTRelative(input_motion)
  motions = builder.EndVector(len(motion_offsets))

  configurations_offsets = []
  for input_configuration in input_reaction.get_configurations():
    name_string_offset = builder.CreateString(
        input_configuration.get_configurable_name())
    flbmodels.FBSConfigurationStart(builder)
    flbmodels.FBSConfigurationAddConfigurableName(builder,
                                                  name_string_offset)
    flbmodels.FBSConfigurationAddConfigurableValue(builder,
                                                   input_configuration.get_configurable_value())
    configuration_offset = flbmodels.FBSMotionEnd(builder)
    configurations_offsets.append(configuration_offset)

  flbmodels.FBSReactionStartMotionsVector(builder,
                                          len(configurations_offsets))
  for input_configuration in configurations_offsets:
    builder.PrependUOffsetTRelative(input_configuration)
  configurations = builder.EndVector(len(configurations_offsets))

  flbmodels.FBSReactionStart(builder)
  flbmodels.FBSReactionAddReset(builder, input_reaction.get_reset())
  flbmodels.FBSReactionAddMotions(builder, motions)
  flbmodels.FBSReactionAddConfigurations(builder, configurations)
  flat_reaction = flbmodels.FBSReactionEnd(builder)
  builder.Finish(flat_reaction)
  return builder.Output()


def deserialize_state(state):
  s = flbmodels.FBSState.GetRootAsFBSState(state, 0)
  return s


def create_state(flat_state):
  state = neomodels.EnvironmentState(flat_state)
  return state


def create_actors(flat_state):
  actors = {}
  for i in range(1, flat_state.ActorsLength() + 1):
    flat_actor = flat_state.Actors(i)
    motors = create_motors(flat_actor)
    input_actor = neomodels.Actor(
        flat_actor.ActorName(),
        motors)
    actors[input_actor.get_name()] = input_actor
  return actors


def create_observers(flat_state):
  observers = {}
  for i in range(1, flat_state.ObserversLength() + 1):
    flat_observer = flat_state.Observers(i)
    transform = flat_observer.Transform()
    position = transform.Position(FBSVec3())
    rotation = transform.Rotation(FBSVec3())
    direction = transform.Direction(FBSVec3())
    body = flat_observer.Body()
    velocity = body.Velocity(FBSVec3())
    angular_velocity = body.AngularVelocity(FBSVec3())
    data = create_data(flat_observer)
    input_observer = neomodels.Observer(
        flat_observer.ObserverName(),
        data,
        [position.X(), position.Y(), position.Z()],
        [rotation.X(), rotation.Y(), rotation.Z()],
        [direction.X(), direction.Y(), direction.Z()],
        [velocity.X(), velocity.Y(), velocity.Z()],
        [angular_velocity.X(), angular_velocity.Y(), angular_velocity.Z()]
    )
    observers[input_observer.get_name()] = input_observer
  return observers


def create_configurables(flat_state):
  configurables = {}
  for i in range(1, flat_state.ConfigurablesLength() + 1):
    fbs_configurable = flat_state.Configurables(i)
    configurable = neomodels.Configurable(
        fbs_configurable.ConfigurableName(),
        fbs_configurable.ConfigurableName())
    configurables[configurable.get_configurable_name()] = fbs_configurable
  return configurables


def create_data(flat_observer):
  data = np.array(
      [
        flat_observer.Data(i)
        for i in range(4, flat_observer.DataLength() + 4)  # 4 and -4 Strips
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
    input_motor = neomodels.Motor(flat_motor.MotorName(),
                                  flat_motor.ValidInput(),
                                  flat_motor.EnergyCost(),
                                  flat_motor.EnergySpentSinceReset())
    motors[input_motor.get_name()] = input_motor
  return motors
