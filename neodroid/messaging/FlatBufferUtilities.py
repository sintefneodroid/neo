from .FlatBufferModels import *

def build_flat_reaction(reaction):
  builder = flatbuffers.Builder(0)

  motion_offsets = []
  for motion in reaction._actor_motor_motions:
    FlatBufferMotionStart(builder)
    FlatBufferMotionAddActorName(builder, motion._actor_name)
    FlatBufferMotionAddMotorName(builder, motion._motor_name)
    FlatBufferMotionAddStrength(builder, motion._strength)
    motion_offset = FlatBufferMotionEnd(builder)
    motion_offsets.append(motion_offset)

  FlatBufferReactionStartMotionsVector(builder, len(motion_offsets))
  for motion in motion_offsets:
    builder.PrependUOffsetTRelative(motion)
  motions = builder.EndVector(len(motion_offsets))

  FlatBufferReactionStart(builder)
  FlatBufferReactionAddReset(builder, reaction._reset)
  FlatBufferReactionAddMotions(builder, motions)
  flat_reaction = FlatBufferReactionEnd(builder)
  builder.Finish(flat_reaction)
  return builder.Output()

def deserialize_state(state):
  s = FlatBufferState.GetRootAsFlatBufferState(state, 0)
  return s

def create_state(state):

  pass
def create_actor(actor):

  pass
def create_observer(observer):

  pass
def create_motor(motor):

  pass
