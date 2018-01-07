# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBS

import flatbuffers


class FBSUnobservables(object):
  __slots__ = ['_tab']

  @classmethod
  def GetRootAsFBSUnobservables(cls, buf, offset):
    n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
    x = FBSUnobservables()
    x.Init(buf, n + offset)
    return x

  # FBSUnobservables
  def Init(self, buf, pos):
    self._tab = flatbuffers.table.Table(buf, pos)

  # FBSUnobservables
  def Poses(self, j):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
    if o != 0:
      x = self._tab.Vector(o)
      x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 56
      from .FBSQuaternionTransform import FBSQuaternionTransform
      obj = FBSQuaternionTransform()
      obj.Init(self._tab.Bytes, x)
      return obj
    return None

  # FBSUnobservables
  def PosesLength(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
    if o != 0:
      return self._tab.VectorLen(o)
    return 0

  # FBSUnobservables
  def Bodies(self, j):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
    if o != 0:
      x = self._tab.Vector(o)
      x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 48
      from .FBSBody import FBSBody
      obj = FBSBody()
      obj.Init(self._tab.Bytes, x)
      return obj
    return None

  # FBSUnobservables
  def BodiesLength(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
    if o != 0:
      return self._tab.VectorLen(o)
    return 0


def FBSUnobservablesStart(builder): builder.StartObject(2)


def FBSUnobservablesAddPoses(builder, poses): builder.PrependUOffsetTRelativeSlot(0,
                                                                                  flatbuffers.number_types.UOffsetTFlags.py_type(
                                                                                    poses), 0)


def FBSUnobservablesStartPosesVector(builder, numElems): return builder.StartVector(56, numElems, 8)


def FBSUnobservablesAddBodies(builder, bodies): builder.PrependUOffsetTRelativeSlot(1,
                                                                                    flatbuffers.number_types.UOffsetTFlags.py_type(
                                                                                      bodies), 0)


def FBSUnobservablesStartBodiesVector(builder, numElems): return builder.StartVector(48, numElems, 8)


def FBSUnobservablesEnd(builder): return builder.EndObject()
