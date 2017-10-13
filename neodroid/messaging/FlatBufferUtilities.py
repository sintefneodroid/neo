from io import BytesIO

import numpy as np

from neodroid.models import *
from .FlatBufferModels import *


def build_flat_reaction(input_reaction):
  builder = flatbuffers.Builder(0)

  motion_offsets = []
  for input_motion in input_reaction.get_motions:
    actor_string_offset = builder.CreateString(input_motion.get_actor_name)
    motor_string_offset = builder.CreateString(input_motion.get_motor_name)
    FlatBufferMotionStart(builder)
    FlatBufferMotionAddActorName(builder, actor_string_offset)
    FlatBufferMotionAddMotorName(builder, motor_string_offset)
    FlatBufferMotionAddStrength(builder, input_motion.get_strength)
    motion_offset = FlatBufferMotionEnd(builder)
    motion_offsets.append(motion_offset)

  FlatBufferReactionStartMotionsVector(builder, len(motion_offsets))
  for input_motion in motion_offsets:
    builder.PrependUOffsetTRelative(input_motion)
  motions = builder.EndVector(len(motion_offsets))

  FlatBufferReactionStart(builder)
  FlatBufferReactionAddReset(builder, input_reaction.get_reset)
  FlatBufferReactionAddMotions(builder, motions)
  flat_reaction = FlatBufferReactionEnd(builder)
  builder.Finish(flat_reaction)
  return builder.Output()


def deserialize_state(state):
  s = FlatBufferState.GetRootAsFlatBufferState(state, 0)
  return s


def create_state(flat_state):
  state = EnvironmentState(flat_state.TimeSinceRest(), flat_state.TotalEnergySpentSinceReset(), create_actors(
      flat_state), create_observers(flat_state), flat_state.RewardForLastStep())
  return state


def create_actors(flat_state):
  actors = []
  for i in range(1, flat_state.ActorsLength() + 1):
    flat_actor = flat_state.Actors(i)
    motors = create_motors(flat_actor)
    pos_rot = flat_actor.Posrot()
    position = pos_rot.Position()
    rotation = pos_rot.Rotation()
    input_actor = Actor(flat_actor.Name(), [position.X(), position.Y(), position.Z()],
                  [rotation.X(), rotation.Y(), rotation.Z(),
                   rotation.W()], motors)
    actors.append(input_actor)
  return actors


def create_observers(flat_state):
  observers = []
  for i in range(1, flat_state.ObserversLength() + 1):
    flat_observer = flat_state.Observers(i)
    pos_rot = flat_observer.Posrot()
    position = pos_rot.Position()
    rotation = pos_rot.Rotation()
    data = create_data(flat_observer)
    input_observer = Observer(flat_observer.Name(), data, [position.X(), position.Y(), position.Z()],
                              [rotation.X(), rotation.Y(), rotation.Z(),
                               rotation.W()], )
    observers.append(input_observer)
  return observers


def create_data(flat_observer):
  data = np.array([flat_observer.Data(i) for i in range(4, flat_observer.DataLength() - 4)],
                  dtype=np.uint8).tobytes()  # Weird magic sizes
  bytes_stream = BytesIO(data)
  # bytes_stream.seek(0)
  return bytes_stream


def create_motors(flat_actor):
  motors = []
  for i in range(1, flat_actor.MotorsLength() + 1):
    flat_motor = flat_actor.Motors(i)
    input_motor = Motor(flat_motor.Name(), flat_motor.Binary(), flat_motor.EnergyCost(),
                        flat_motor.EnergySpentSinceReset())
    motors.append(input_motor)
  return motors
