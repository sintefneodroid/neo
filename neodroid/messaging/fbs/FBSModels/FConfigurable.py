# automatically generated by the FlatBuffers compiler, do not modify

# namespace: State

import flatbuffers


class FConfigurable(object):
    __slots__ = ["_tab"]

    @classmethod
    def GetRootAsFConfigurable(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = FConfigurable()
        x.Init(buf, n + offset)
        return x

    # FConfigurable
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # FConfigurable
    def ConfigurableName(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return

    # FConfigurable
    def ConfigurableValueType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # FConfigurable
    def ConfigurableValue(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            from flatbuffers.table import Table

            obj = Table(bytearray(), 0)
            self._tab.Union(obj, o)
            return obj
        return

    # FConfigurable
    def ConfigurableRange(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            x = o + self._tab.Pos
            from .FRange import FRange

            obj = FRange()
            obj.Init(self._tab.Bytes, x)
            return obj
        return


def FConfigurableStart(builder):
    builder.StartObject(4)


def FConfigurableAddConfigurableName(builder, configurableName):
    builder.PrependUOffsetTRelativeSlot(
        0, flatbuffers.number_types.UOffsetTFlags.py_type(configurableName), 0
    )


def FConfigurableAddConfigurableValueType(builder, configurableValueType):
    builder.PrependUint8Slot(1, configurableValueType, 0)


def FConfigurableAddConfigurableValue(builder, configurableValue):
    builder.PrependUOffsetTRelativeSlot(
        2, flatbuffers.number_types.UOffsetTFlags.py_type(configurableValue), 0
    )


def FConfigurableAddConfigurableRange(builder, configurableRange):
    builder.PrependStructSlot(
        3, flatbuffers.number_types.UOffsetTFlags.py_type(configurableRange), 0
    )


def FConfigurableEnd(builder):
    return builder.EndObject()
