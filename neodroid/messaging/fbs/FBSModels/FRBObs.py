# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBS

import flatbuffers


class FRBObs(object):
    __slots__ = ["_tab"]

    @classmethod
    def GetRootAsFRBObs(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = FRBObs()
        x.Init(buf, n + offset)
        return x

    # FRBObs
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # FRBObs
    def Body(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = o + self._tab.Pos
            from .FBody import FBody

            obj = FBody()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # FRBObs
    def VelRange(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = o + self._tab.Pos
            from .FRange import FRange

            obj = FRange()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # FRBObs
    def AngRange(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = o + self._tab.Pos
            from .FRange import FRange

            obj = FRange()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None


def FRBObsStart(builder):
    builder.StartObject(3)


def FRBObsAddBody(builder, body):
    builder.PrependStructSlot(
        0, flatbuffers.number_types.UOffsetTFlags.py_type(body), 0
    )


def FRBObsAddVelRange(builder, velRange):
    builder.PrependStructSlot(
        1, flatbuffers.number_types.UOffsetTFlags.py_type(velRange), 0
    )


def FRBObsAddAngRange(builder, angRange):
    builder.PrependStructSlot(
        2, flatbuffers.number_types.UOffsetTFlags.py_type(angRange), 0
    )


def FRBObsEnd(builder):
    return builder.EndObject()
