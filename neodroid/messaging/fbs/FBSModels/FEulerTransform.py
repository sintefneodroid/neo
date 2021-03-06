# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBS

import flatbuffers


class FEulerTransform(object):
    __slots__ = ["_tab"]

    # FEulerTransform
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # FEulerTransform
    def Position(self, obj):
        obj.Init(self._tab.Bytes, self._tab.Pos + 0)
        return obj

    # FEulerTransform
    def Rotation(self, obj):
        obj.Init(self._tab.Bytes, self._tab.Pos + 24)
        return obj

    # FEulerTransform
    def Direction(self, obj):
        obj.Init(self._tab.Bytes, self._tab.Pos + 48)
        return obj


def CreateFEulerTransform(
    builder,
    position_x,
    position_y,
    position_z,
    rotation_x,
    rotation_y,
    rotation_z,
    direction_x,
    direction_y,
    direction_z,
):
    builder.Prep(8, 72)
    builder.Prep(8, 24)
    builder.PrependFloat64(direction_z)
    builder.PrependFloat64(direction_y)
    builder.PrependFloat64(direction_x)
    builder.Prep(8, 24)
    builder.PrependFloat64(rotation_z)
    builder.PrependFloat64(rotation_y)
    builder.PrependFloat64(rotation_x)
    builder.Prep(8, 24)
    builder.PrependFloat64(position_z)
    builder.PrependFloat64(position_y)
    builder.PrependFloat64(position_x)
    return builder.Offset()
