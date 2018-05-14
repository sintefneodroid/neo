# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBS

import flatbuffers


class FTriple(object):
  __slots__ = ['_tab']

  @classmethod
  def GetRootAsFTriple(cls, buf, offset):
    n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
    x = FTriple()
    x.Init(buf, n + offset)
    return x

  # FTriple
  def Init(self, buf, pos):
    self._tab = flatbuffers.table.Table(buf, pos)

  # FTriple
  def Vec3(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
    if o != 0:
      x = o + self._tab.Pos
      from .FVector3 import FVector3
      obj = FVector3()
      obj.Init(self._tab.Bytes, x)
      return obj
    return None

  # FTriple
  def XRange(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
    if o != 0:
      x = o + self._tab.Pos
      from .FRange import FRange
      obj = FRange()
      obj.Init(self._tab.Bytes, x)
      return obj
    return None

  # FTriple
  def YRange(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
    if o != 0:
      x = o + self._tab.Pos
      from .FRange import FRange
      obj = FRange()
      obj.Init(self._tab.Bytes, x)
      return obj
    return None

  # FTriple
  def ZRange(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
    if o != 0:
      x = o + self._tab.Pos
      from .FRange import FRange
      obj = FRange()
      obj.Init(self._tab.Bytes, x)
      return obj
    return None


def FTripleStart(builder): builder.StartObject(4)


def FTripleAddVec3(builder, vec3): builder.PrependStructSlot(0,
                                                             flatbuffers.number_types.UOffsetTFlags.py_type(
                                                                 vec3), 0)


def FTripleAddXRange(builder, xRange): builder.PrependStructSlot(1,
                                                                 flatbuffers.number_types.UOffsetTFlags.py_type(
                                                                     xRange), 0)


def FTripleAddYRange(builder, yRange): builder.PrependStructSlot(2,
                                                                 flatbuffers.number_types.UOffsetTFlags.py_type(
                                                                     yRange), 0)


def FTripleAddZRange(builder, zRange): builder.PrependStructSlot(3,
                                                                 flatbuffers.number_types.UOffsetTFlags.py_type(
                                                                     zRange), 0)


def FTripleEnd(builder): return builder.EndObject()
