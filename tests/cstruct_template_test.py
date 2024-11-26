import ctypes
import struct
from binascii import hexlify
from ctypes import (c_uint16, c_uint32, c_uint8, Structure)
from typing import cast

import pytest

from sensirion_driver_support_types.cstruct_template import (CStructTemplate, little_endian, big_endian, LittleEndian)


class MisAlignedStructure(metaclass=CStructTemplate):
    f1: c_uint32 = 0xAABBCCDD
    f2: c_uint8 = 0x99
    f3: c_uint32 = 0x88776655


@big_endian
class SimpleBigEndian(metaclass=CStructTemplate):
    f1: c_uint16 = 0xA55A
    f2: c_uint16 = 0xbbaa


@little_endian
class SimpleLittleEndian(metaclass=CStructTemplate):
    f1: c_uint16 = 0xA55A
    f2: c_uint16 = 0x55AA


ByteArray4 = c_uint8 * 4


@little_endian
class NestedStruct(metaclass=CStructTemplate):
    f1: c_uint32 = c_uint32(0x89ABCDEF)
    ba: ByteArray4 = ByteArray4(1, 2, 3, 4)
    s1: SimpleLittleEndian = SimpleLittleEndian(f1=0xBBBB)
    s2: SimpleLittleEndian = SimpleLittleEndian(f2=0xBBBB)


@pytest.mark.parametrize("struct_type", [
    SimpleLittleEndian,
    SimpleBigEndian,
    NestedStruct,
    MisAlignedStructure[LittleEndian]
])
def test_to_bytes_from_bytes(struct_type):
    obj = struct_type()
    byte_data = bytes(obj)
    new_obj = struct_type.from_bytes(byte_data)
    assert repr(obj) == repr(new_obj)


def test_little_big_endian():
    big_e = SimpleBigEndian()
    little_e = SimpleLittleEndian()
    assert (bytes(big_e) != bytes(little_e))


@pytest.mark.parametrize("f1, f2", [
    (0xA55A, 0xbbaa),
])
def test_big_endian(f1, f2):
    packed_data = hexlify(struct.pack(">HH", f1, f2))
    big_e = SimpleBigEndian(f2=f2)
    big_e_data = hexlify(bytes(big_e))
    assert (big_e_data == packed_data)


@pytest.mark.parametrize("f1, f2", [
    (0xA55A, 0xbbaa),
])
def test_little_endian(f1, f2):
    packed_data = hexlify(struct.pack("<HH", f1, f2))
    big_e = SimpleLittleEndian(f2=f2)
    big_e_data = hexlify(bytes(big_e))
    assert (big_e_data == packed_data)


def test_ctor():
    big_e = SimpleBigEndian(f1=0xaaaa)
    assert big_e.f1 == 0xaaaa
    assert big_e.f2 == int(big_e.get_defaults()['f2'])


@pytest.mark.parametrize("pack, size", [
    (1, 9),
    (2, 10),
    (4, 12)])
def test_packing(pack, size):
    c_obj = cast(Structure, MisAlignedStructure[LittleEndian, pack]())
    assert (ctypes.sizeof(c_obj) == size)


def test_repr():
    big_e = SimpleBigEndian(f1=0xaaaa)
    big_e_repr = repr(big_e)
    expected = """c_struct SimpleBigEndian[B1] {
    f1 : 43690
    f2 : 48042
    }"""
    assert (expected == big_e_repr)


def test_fieldnames():
    big_e = SimpleBigEndian(f1=0xaaaa)
    assert ["f1", "f2"] == big_e.get_field_names()
