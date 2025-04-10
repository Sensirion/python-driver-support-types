# -*- coding: utf-8 -*-
import pytest

from sensirion_driver_support_types.bitfield import BitField, BitfieldContainer


class StatusWord(BitfieldContainer):
    gas_conc = BitField(offset=0, width=10)
    avg_mode_flag = BitField(offset=10, width=1)
    exp_smoothing_flag = BitField(offset=11, width=1)
    command_code = BitField(offset=12, width=4)


@pytest.mark.parametrize("value, expected_val, fields",
                         [(StatusWord(0), 0,
                           {'gas_conc': 0, 'avg_mode_flag': 0,
                            'exp_smoothing_flag': 0, 'command_code': 0}),
                          (StatusWord(0xFFFF), 0xFFFF,
                           {'gas_conc': 1023, 'avg_mode_flag': 1,
                            'exp_smoothing_flag': 1, 'command_code': 15})
                          ])
def test_bitfield_decorator_get(value: BitfieldContainer, expected_val, fields):
    assert isinstance(value, BitfieldContainer)
    assert value.value == expected_val
    for name, int_val in fields.items():
        attr = getattr(value, name)
        assert attr == int_val


def test_bitfield_decorator_set():
    sw = StatusWord(0)
    sw.gas_conc = 516
    sw.exp_smoothing_flag = 1
    sw.avg_mode_flag = 1
    sw.command_code = 12
    assert sw.command_code == 12
    assert sw.avg_mode_flag == 1
    assert sw.exp_smoothing_flag == 1
    assert sw.gas_conc == 516
    assert sw.value == 0b1100111000000100


def test_bitfield_decorator_init():
    sw = StatusWord(gas_conc=516, exp_smoothing_flag=1, avg_mode_flag=1, command_code=12)
    assert sw.command_code == 12
    assert sw.avg_mode_flag == 1
    assert sw.exp_smoothing_flag == 1
    assert sw.gas_conc == 516
    assert sw.value == 0b1100111000000100


def test_bitfield_to_str():
    sw = StatusWord(0)
    assert str(sw) == "{gas_conc: 0x0, avg_mode_flag: 0x0, exp_smoothing_flag: 0x0, command_code: 0x0}"


def test_bitfield_to_int():
    sw = StatusWord(0)
    assert int(sw) == 0
