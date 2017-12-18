# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Reaction

import flatbuffers

class FBSReaction(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsFBSReaction(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = FBSReaction()
        x.Init(buf, n + offset)
        return x

    # FBSReaction
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # FBSReaction
    def EnvironmentName(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return bytes()

    # FBSReaction
    def Reset(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos)
        return 0

    # FBSReaction
    def ActionType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # FBSReaction
    def Action(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            from flatbuffers.table import Table
            obj = Table(bytearray(), 0)
            self._tab.Union(obj, o)
            return obj
        return None

def FBSReactionStart(builder): builder.StartObject(4)
def FBSReactionAddEnvironmentName(builder, environmentName): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(environmentName), 0)
def FBSReactionAddReset(builder, reset): builder.PrependBoolSlot(1, reset, 0)
def FBSReactionAddActionType(builder, actionType): builder.PrependUint8Slot(2, actionType, 0)
def FBSReactionAddAction(builder, action): builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(action), 0)
def FBSReactionEnd(builder): return builder.EndObject()
