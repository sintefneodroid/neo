# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBS

import flatbuffers


class FBSRotation(object):
  __slots__ = ['_tab']

  @classmethod
  def GetRootAsFBSRotation(cls, buf, offset):
    n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
    x = FBSRotation()
    x.Init(buf, n + offset)
    return x

  # FBSRotation
  def Init(self, buf, pos):
    self._tab = flatbuffers.table.Table(buf, pos)

  # FBSRotation
  def Rotation(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
    if o != 0:
      x = o + self._tab.Pos
      from .FBSVector3 import FBSVector3
      obj = FBSVector3()
      obj.Init(self._tab.Bytes, x)
      return obj
    return None


def FBSRotationStart(builder): builder.StartObject(1)


def FBSRotationAddRotation(builder, rotation): builder.PrependStructSlot(0,
                                                                         flatbuffers.number_types.UOffsetTFlags.py_type(
                                                                           rotation), 0)


def FBSRotationEnd(builder): return builder.EndObject()
