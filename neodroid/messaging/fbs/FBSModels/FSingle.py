# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBS

import flatbuffers


class FSingle(object):
    __slots__ = ["_tab"]

    @classmethod
    def GetRootAsFSingle(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = FSingle()
        x.Init(buf, n + offset)
        return x

    # FSingle
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # FSingle
    def Value(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(
                flatbuffers.number_types.Float64Flags, o + self._tab.Pos
            )
        return 0.0

    # FSingle
    def Range(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = o + self._tab.Pos
            from .FRange import FRange

            obj = FRange()
            obj.Init(self._tab.Bytes, x)
            return obj
        return


def FSingleStart(builder):
    builder.StartObject(2)


def FSingleAddValue(builder, value):
    builder.PrependFloat64Slot(0, value, 0.0)


def FSingleAddRange(builder, range):
    builder.PrependStructSlot(
        1, flatbuffers.number_types.UOffsetTFlags.py_type(range), 0
    )


def FSingleEnd(builder):
    return builder.EndObject()
