# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBS

import flatbuffers


class FRange(object):
  __slots__ = ['_tab']

  # FRange
  def Init(self, buf, pos):
    self._tab = flatbuffers.table.Table(buf, pos)

  # FRange
  def DecimalGranularity(self): return self._tab.Get(flatbuffers.number_types.Int32Flags,
                                                     self._tab.Pos +
                                                     flatbuffers.number_types.UOffsetTFlags.py_type(
                                                       0))

  # FRange
  def MaxValue(self): return self._tab.Get(flatbuffers.number_types.Float32Flags,
                                           self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4))

  # FRange
  def MinValue(self): return self._tab.Get(flatbuffers.number_types.Float32Flags,
                                           self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(8))


def CreateFRange(builder, decimalGranularity, maxValue, minValue):
  builder.Prep(4, 12)
  builder.PrependFloat32(minValue)
  builder.PrependFloat32(maxValue)
  builder.PrependInt32(decimalGranularity)
  return builder.Offset()
