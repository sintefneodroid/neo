# automatically generated by the FlatBuffers compiler, do not modify

# namespace: State

import flatbuffers


class FActor(object):
  __slots__ = ['_tab']

  @classmethod
  def GetRootAsFActor(cls, buf, offset):
    n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
    x = FActor()
    x.Init(buf, n + offset)
    return x

  # FActor
  def Init(self, buf, pos):
    self._tab = flatbuffers.table.Table(buf, pos)

  # FActor
  def ActorName(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
    if o != 0:
      return self._tab.String(o + self._tab.Pos)
    return bytes()

  # FActor
  def Alive(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
    if o != 0:
      return self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos)
    return 0

  # FActor
  def Motors(self, j):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
    if o != 0:
      x = self._tab.Vector(o)
      x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
      x = self._tab.Indirect(x)
      from .FMotor import FMotor
      obj = FMotor()
      obj.Init(self._tab.Bytes, x)
      return obj
    return None

  # FActor
  def MotorsLength(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
    if o != 0:
      return self._tab.VectorLen(o)
    return 0


def FActorStart(builder): builder.StartObject(3)


def FActorAddActorName(builder, actorName): builder.PrependUOffsetTRelativeSlot(0,
                                                                                flatbuffers.number_types.UOffsetTFlags.py_type(
                                                                                    actorName), 0)


def FActorAddAlive(builder, alive): builder.PrependBoolSlot(1, alive, 0)


def FActorAddMotors(builder, motors): builder.PrependUOffsetTRelativeSlot(2,
                                                                          flatbuffers.number_types.UOffsetTFlags.py_type(
                                                                              motors), 0)


def FActorStartMotorsVector(builder, numElems): return builder.StartVector(4, numElems, 4)


def FActorEnd(builder): return builder.EndObject()