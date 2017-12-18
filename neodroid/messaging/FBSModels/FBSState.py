# automatically generated by the FlatBuffers compiler, do not modify

# namespace: State

import flatbuffers

class FBSState(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsFBSState(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = FBSState()
        x.Init(buf, n + offset)
        return x

    # FBSState
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # FBSState
    def EnvironmentName(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return bytes()

    # FBSState
    def FrameNumber(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # FBSState
    def Reward(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # FBSState
    def Interrupted(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos)
        return 0

    # FBSState
    def TotalEnergySpent(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # FBSState
    def Observers(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .FBSObserver import FBSObserver
            obj = FBSObserver()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # FBSState
    def ObserversLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # FBSState
    def EnvironmentDescription(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from .FBSEnvironmentDescription import FBSEnvironmentDescription
            obj = FBSEnvironmentDescription()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # FBSState
    def DebugMessage(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return bytes()

def FBSStateStart(builder): builder.StartObject(8)
def FBSStateAddEnvironmentName(builder, environmentName): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(environmentName), 0)
def FBSStateAddFrameNumber(builder, frameNumber): builder.PrependInt32Slot(1, frameNumber, 0)
def FBSStateAddReward(builder, reward): builder.PrependFloat32Slot(2, reward, 0.0)
def FBSStateAddInterrupted(builder, interrupted): builder.PrependBoolSlot(3, interrupted, 0)
def FBSStateAddTotalEnergySpent(builder, totalEnergySpent): builder.PrependFloat32Slot(4, totalEnergySpent, 0.0)
def FBSStateAddObservers(builder, observers): builder.PrependUOffsetTRelativeSlot(5, flatbuffers.number_types.UOffsetTFlags.py_type(observers), 0)
def FBSStateStartObserversVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def FBSStateAddEnvironmentDescription(builder, environmentDescription): builder.PrependUOffsetTRelativeSlot(6, flatbuffers.number_types.UOffsetTFlags.py_type(environmentDescription), 0)
def FBSStateAddDebugMessage(builder, debugMessage): builder.PrependUOffsetTRelativeSlot(7, flatbuffers.number_types.UOffsetTFlags.py_type(debugMessage), 0)
def FBSStateEnd(builder): return builder.EndObject()
