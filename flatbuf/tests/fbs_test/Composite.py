# automatically generated by the FlatBuffers compiler, do not modify

# namespace: fbs_test

import flatbuffers

class Composite(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsComposite(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Composite()
        x.Init(buf, n + offset)
        return x

    # Composite
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Composite
    def Shade(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = o + self._tab.Pos
            from .Color import Color
            obj = Color()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Composite
    def Name(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return ""

    # Composite
    def RefData(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .Identity import Identity
            obj = Identity()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Composite
    def RefDataLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Composite
    def Loc(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            x = o + self._tab.Pos
            from .Location import Location
            obj = Location()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Composite
    def Bytes(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Composite
    def BytesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def CompositeStart(builder): builder.StartObject(5)
def CompositeAddShade(builder, shade): builder.PrependStructSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(shade), 0)
def CompositeAddName(builder, name): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(name), 0)
def CompositeAddRefData(builder, refData): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(refData), 0)
def CompositeStartRefDataVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def CompositeAddLoc(builder, loc): builder.PrependStructSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(loc), 0)
def CompositeAddBytes(builder, bytes): builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(bytes), 0)
def CompositeStartBytesVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def CompositeEnd(builder): return builder.EndObject()