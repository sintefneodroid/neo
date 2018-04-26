# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBS

import flatbuffers


class FSimulatorConfiguration(object):
  __slots__ = ['_tab']

  # FSimulatorConfiguration
  def Init(self, buf, pos):
    self._tab = flatbuffers.table.Table(buf, pos)

  # FSimulatorConfiguration
  def Width(self):
    return self._tab.Get(
        flatbuffers.number_types.Int32Flags,
        self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0),
        )

  # FSimulatorConfiguration
  def Height(self):
    return self._tab.Get(
        flatbuffers.number_types.Int32Flags,
        self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4),
        )

  # FSimulatorConfiguration
  def FullScreen(self):
    return self._tab.Get(
        flatbuffers.number_types.BoolFlags,
        self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(8),
        )

  # FSimulatorConfiguration
  def QualityLevel(self):
    return self._tab.Get(
        flatbuffers.number_types.Int32Flags,
        self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(12),
        )

  # FSimulatorConfiguration
  def TimeScale(self):
    return self._tab.Get(
        flatbuffers.number_types.Float32Flags,
        self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(16),
        )

  # FSimulatorConfiguration
  def TargetFrameRate(self):
    return self._tab.Get(
        flatbuffers.number_types.Float32Flags,
        self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(20),
        )

  # FSimulatorConfiguration
  def WaitEvery(self):
    return self._tab.Get(
        flatbuffers.number_types.Int32Flags,
        self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(24),
        )

  # FSimulatorConfiguration
  def FrameSkips(self):
    return self._tab.Get(
        flatbuffers.number_types.Int32Flags,
        self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(28),
        )

  # FSimulatorConfiguration
  def ResetIterations(self):
    return self._tab.Get(
        flatbuffers.number_types.Int32Flags,
        self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(32),
        )


def CreateFSimulatorConfiguration(
    builder,
    width,
    height,
    fullScreen,
    qualityLevel,
    timeScale,
    targetFrameRate,
    waitEvery,
    frameSkips,
    resetIterations,
    ):
  builder.Prep(4, 36)
  builder.PrependInt32(resetIterations)
  builder.PrependInt32(frameSkips)
  builder.PrependInt32(waitEvery)
  builder.PrependFloat32(targetFrameRate)
  builder.PrependFloat32(timeScale)
  builder.PrependInt32(qualityLevel)
  builder.Pad(3)
  builder.PrependBool(fullScreen)
  builder.PrependInt32(height)
  builder.PrependInt32(width)
  return builder.Offset()
