# automatically generated by the FlatBuffers compiler, do not modify

# namespace: State

import flatbuffers

class FBSConfigurable(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsFBSConfigurable(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = FBSConfigurable()
        x.Init(buf, n + offset)
        return x

    # FBSConfigurable
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # FBSConfigurable
    def ConfigurableName(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return bytes()

    # FBSConfigurable
    def HasObserver(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos)
        return 0

    # FBSConfigurable
    def ObserverName(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return bytes()

    # FBSConfigurable
    def ValidInput(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            x = o + self._tab.Pos
            from .FBSRange import FBSRange
            obj = FBSRange()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def FBSConfigurableStart(builder): builder.StartObject(4)
def FBSConfigurableAddConfigurableName(builder, configurableName): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(configurableName), 0)
def FBSConfigurableAddHasObserver(builder, hasObserver): builder.PrependBoolSlot(1, hasObserver, 0)
def FBSConfigurableAddObserverName(builder, observerName): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(observerName), 0)
def FBSConfigurableAddValidInput(builder, validInput): builder.PrependStructSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(validInput), 0)
def FBSConfigurableEnd(builder): return builder.EndObject()