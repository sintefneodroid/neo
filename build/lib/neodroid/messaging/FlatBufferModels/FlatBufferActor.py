# automatically generated by the FlatBuffers compiler, do not modify

# namespace: State

import flatbuffers


class FlatBufferActor(object):
  __slots__ = ['_tab']

  @classmethod
  def GetRootAsFlatBufferActor(cls, buf, offset):
    n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
    x = FlatBufferActor()
    x.Init(buf, n + offset)
    return x

  # FlatBufferActor
  def Init(self, buf, pos):
    self._tab = flatbuffers.table.Table(buf, pos)

  # FlatBufferActor
  def Name(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
    if o != 0:
      return self._tab.String(o + self._tab.Pos)
    return ""

  # FlatBufferActor
  def Posrot(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
    if o != 0:
      x = self._tab.Indirect(o + self._tab.Pos)
      from .FlatBufferPosRot import FlatBufferPosRot
      obj = FlatBufferPosRot()
      obj.Init(self._tab.Bytes, x)
      return obj
    return None

  # FlatBufferActor
  def Motors(self, j):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
    if o != 0:
      x = self._tab.Vector(o)
      x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
      x = self._tab.Indirect(x)
      from .FlatBufferMotor import FlatBufferMotor
      obj = FlatBufferMotor()
      obj.Init(self._tab.Bytes, x)
      return obj
    return None

  # FlatBufferActor
  def MotorsLength(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
    if o != 0:
      return self._tab.VectorLen(o)
    return 0


def FlatBufferActorStart(builder): builder.StartObject(3)


def FlatBufferActorAddName(builder, name): builder.PrependUOffsetTRelativeSlot(
    0,
    flatbuffers.number_types.UOffsetTFlags.py_type(
        name), 0)


def FlatBufferActorAddPosrot(builder,
                             posrot): builder.PrependUOffsetTRelativeSlot(1,
                                                                          flatbuffers.number_types.UOffsetTFlags.py_type(
                                                                              posrot),
                                                                          0)


def FlatBufferActorAddMotors(builder,
                             motors): builder.PrependUOffsetTRelativeSlot(2,
                                                                          flatbuffers.number_types.UOffsetTFlags.py_type(
                                                                              motors),
                                                                          0)


def FlatBufferActorStartMotorsVector(builder,
                                     numElems): return builder.StartVector(4,
                                                                           numElems,
                                                                           4)


def FlatBufferActorEnd(builder): return builder.EndObject()
