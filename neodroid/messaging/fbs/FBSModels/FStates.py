# automatically generated by the FlatBuffers compiler, do not modify

# namespace: State

import flatbuffers


class FStates(object):
    __slots__ = ["_tab"]

    @classmethod
    def GetRootAsFStates(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = FStates()
        x.Init(buf, n + offset)
        return x

    # FStates
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # FStates
    def States(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .FState import FState

            obj = FState()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # FStates
    def StatesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # FStates
    def ApiVersion(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # FStates
    def SimulatorConfiguration(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = o + self._tab.Pos
            from .FSimulatorConfiguration import FSimulatorConfiguration

            obj = FSimulatorConfiguration()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None


def FStatesStart(builder):
    builder.StartObject(3)


def FStatesAddStates(builder, states):
    builder.PrependUOffsetTRelativeSlot(
        0, flatbuffers.number_types.UOffsetTFlags.py_type(states), 0
    )


def FStatesStartStatesVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)


def FStatesAddApiVersion(builder, apiVersion):
    builder.PrependUOffsetTRelativeSlot(
        1, flatbuffers.number_types.UOffsetTFlags.py_type(apiVersion), 0
    )


def FStatesAddSimulatorConfiguration(builder, simulatorConfiguration):
    builder.PrependStructSlot(
        2, flatbuffers.number_types.UOffsetTFlags.py_type(simulatorConfiguration), 0
    )


def FStatesEnd(builder):
    return builder.EndObject()
