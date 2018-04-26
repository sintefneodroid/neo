# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Reaction

import flatbuffers


class FDisplayable(object):
  __slots__ = ['_tab']

  @classmethod
  def GetRootAsFDisplayable(cls, buf, offset):
    n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
    x = FDisplayable()
    x.Init(buf, n + offset)
    return x

  # FDisplayable
  def Init(self, buf, pos):
    self._tab = flatbuffers.table.Table(buf, pos)

  # FDisplayable
  def DisplayableName(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
    if o != 0:
      return self._tab.String(o + self._tab.Pos)
    return bytes()

  # FDisplayable
  def DisplayableValueType(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
    if o != 0:
      return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
    return 0

  # FDisplayable
  def DisplayableValue(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
    if o != 0:
      from flatbuffers.table import Table

      obj = Table(bytearray(), 0)
      self._tab.Union(obj, o)
      return obj
    return None


def FDisplayableStart(builder):
  builder.StartObject(3)


def FDisplayableAddDisplayableName(builder, displayableName):
  builder.PrependUOffsetTRelativeSlot(
      0, flatbuffers.number_types.UOffsetTFlags.py_type(displayableName), 0
      )


def FDisplayableAddDisplayableValueType(builder, displayableValueType):
  builder.PrependUint8Slot(1, displayableValueType, 0)


def FDisplayableAddDisplayableValue(builder, displayableValue):
  builder.PrependUOffsetTRelativeSlot(
      2, flatbuffers.number_types.UOffsetTFlags.py_type(displayableValue), 0
      )


def FDisplayableEnd(builder):
  return builder.EndObject()
