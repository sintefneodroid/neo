# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBS

import flatbuffers


class FValue(object):
  __slots__ = ['_tab']

  @classmethod
  def GetRootAsFValue(cls, buf, offset):
    n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
    x = FValue()
    x.Init(buf, n + offset)
    return x

  # FValue
  def Init(self, buf, pos):
    self._tab = flatbuffers.table.Table(buf, pos)

  # FValue
  def Val(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
    if o != 0:
      return self._tab.Get(
          flatbuffers.number_types.Float64Flags, o + self._tab.Pos
          )
    return 0.0


def FValueStart(builder):
  builder.StartObject(1)


def FValueAddVal(builder, val):
  builder.PrependFloat64Slot(0, val, 0.0)


def FValueEnd(builder):
  return builder.EndObject()
