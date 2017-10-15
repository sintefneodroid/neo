from io import BytesIO

import flatbuffers as flb
import numpy as np

import neodroid.models as neomodels
from neodroid.messaging import FlatBufferModels as flbmodels


def build_flat_reaction(input_reaction):
  builder = flb.Builder(0)

  motion_offsets = []
  for input_motion in input_reaction.get_motions():
    actor_string_offset = builder.CreateString(
        input_motion.get_actor_name())
    motor_string_offset = builder.CreateString(
        input_motion.get_motor_name())
    flbmodels.FlatBufferMotionStart(builder)
    flbmodels.FlatBufferMotionAddActorName(builder, actor_string_offset)
    flbmodels.FlatBufferMotionAddMotorName(builder, motor_string_offset)
    flbmodels.FlatBufferMotionAddStrength(builder,
                                          input_motion.get_strength())
    motion_offset = flbmodels.FlatBufferMotionEnd(builder)
    motion_offsets.append(motion_offset)

  flbmodels.FlatBufferReactionStartMotionsVector(builder,
                                                 len(motion_offsets))
  for input_motion in motion_offsets:
    builder.PrependUOffsetTRelative(input_motion)
  motions = builder.EndVector(len(motion_offsets))

  flbmodels.FlatBufferReactionStart(builder)
  flbmodels.FlatBufferReactionAddReset(builder, input_reaction.get_reset())
  flbmodels.FlatBufferReactionAddMotions(builder, motions)
  flat_reaction = flbmodels.FlatBufferReactionEnd(builder)
  builder.Finish(flat_reaction)
  return builder.Output()


def deserialize_state(state):
  s = flbmodels.FlatBufferState.GetRootAsFlatBufferState(state, 0)
  return s


def create_state(flat_state):
  state = neomodels.EnvironmentState(flat_state.TimeSinceRest(),
                                     flat_state.TotalEnergySpentSinceReset(),
                                     create_actors(flat_state),
                                     create_observers(flat_state),
                                     flat_state.LastStepsFrameNumber(),
                                     flat_state.RewardForLastStep(),
                                     flat_state.Interrupted())
  return state


def create_actors(flat_state):
  actors = {}
  for i in range(1, flat_state.ActorsLength() + 1):
    flat_actor = flat_state.Actors(i)
    motors = create_motors(flat_actor)
    pos_rot_dir = flat_actor.Posrotdir()
    position = pos_rot_dir.Position()
    rotation = pos_rot_dir.Rotation()
    direction = pos_rot_dir.Direction()
    input_actor = neomodels.Actor(
        flat_actor.Name(), [position.X(), position.Y(), position.Z()],
        [rotation.X(), rotation.Y(), rotation.Z()],
        [direction.X(), direction.Y(), direction.Z()],
        motors)
    actors[input_actor.get_name()] = input_actor
  return actors


def create_observers(flat_state):
  observers = {}
  for i in range(1, flat_state.ObserversLength() + 1):
    flat_observer = flat_state.Observers(i)
    pos_rot_dir = flat_observer.Posrotdir()
    position = pos_rot_dir.Position()
    rotation = pos_rot_dir.Rotation()
    direction = pos_rot_dir.Direction()
    data = create_data(flat_observer)
    input_observer = neomodels.Observer(
        flat_observer.Name(),
        data,
        [position.X(), position.Y(), position.Z()],
        [rotation.X(), rotation.Y(), rotation.Z()],
        [direction.X(), direction.Y(), direction.Z()] )
    observers[input_observer.get_name()] = input_observer
  return observers


def create_data(flat_observer):
  data = np.array(
      [
        flat_observer.Data(i)
        for i in range(4, flat_observer.DataLength() - 4)
      ],
      dtype=np.uint8).tobytes()  # Weird magic sizes
  bytes_stream = BytesIO(data)
  # bytes_stream.seek(0)
  return bytes_stream


def create_motors(flat_actor):
  motors = {}
  for i in range(1, flat_actor.MotorsLength() + 1):
    flat_motor = flat_actor.Motors(i)
    input_motor = neomodels.Motor(flat_motor.Name(),
                                  flat_motor.Binary(),
                                  flat_motor.EnergyCost(),
                                  flat_motor.EnergySpentSinceReset())
    motors[input_motor.get_name()] = input_motor
  return motors
