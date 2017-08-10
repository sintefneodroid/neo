import flatbuffers
from .FlatBufferModels import *

def build_reaction():
  builder = flatbuffers.Builder(0)

  FlatBufferMotionStart(builder)
  motion1 = FlatBufferMotionEnd(builder)

  FlatBufferMotionStart(builder)
  motion2 = FlatBufferMotionEnd(builder)

  FlatBufferReactionStartMotionsVector(builder, 2)
  builder.PrependUOffsetTRelative(motion1)
  builder.PrependUOffsetTRelative(motion2)
  motions = builder.EndVector(2)

  FlatBufferReactionStart(builder)
  FlatBufferReactionAddReset(builder, False)
  FlatBufferReactionAddMotions(builder, motions)
  reaction = FlatBufferReactionEnd(builder)
  builder.Finish(reaction)
  return builder.Output()

def deserialize_state(state):
  s = FlatBufferState.GetRootAsFlatBufferState(state, 0)
  return s