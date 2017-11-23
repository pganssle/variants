from __future__ import division

import math

import pytest

from variants import variants
from ._division_data import DivisionData


class DivisionVariants(object):
    """Example class with variant forms on an instance method."""

    def __init__(self, x):
        self.x = x

    @variants
    def divide(self, y):
        return self.x / y

    @divide.variant('round')
    def divide(self, y):
        return round(self.divide(y))

    @divide.variant('floor')
    def divide(self, y):
        return math.floor(self.divide(y))

    @divide.variant('ceil')
    def divide(self, y):
        return math.ceil(self.divide(y))

    @divide.variant('mode')
    def divide(self, y, mode=None):
        funcs = {
            None: self.divide,
            'floor': self.divide.floor,
            'ceil': self.divide.ceil,
            'round': self.divide.round
        }

        return funcs[mode](y)


@pytest.mark.xfail
@pytest.mark.parametrize('x,y,expected', DivisionData.DIV_VALS)
def test_divide(x, y, expected):
    dv = DivisionVariants(x)
    assert dv.divide(y) == expected



@pytest.mark.xfail
@pytest.mark.parametrize('x,y,expected', DivisionData.ROUND_VALS)
def test_round(x, y, expected):
    dv = DivisionVariants(x)
    assert dv.divide.round(y) == expected




@pytest.mark.xfail
@pytest.mark.parametrize('x,y,expected', DivisionData.FLOOR_VALS)
def test_floor(x, y, expected):
    dv = DivisionVariants(x)
    assert dv.divide.floor(y) == expected




@pytest.mark.xfail
@pytest.mark.parametrize('x,y,expected', DivisionData.CEIL_VALS)
def test_floor(x, y, expected):
    dv = DivisionVariants(x)
    assert dv.divide.floor(y) == expected



@pytest.mark.xfail
@pytest.mark.parametrize('x,y,expected,mode', DivisionData.MODE_VALS)
def test_mode(x, y, expected, mode):
    dv = DivisionVariants(x)
    assert dv.divide.mode(y, mode) == expected


@pytest.mark.xfail
@pytest.mark.parametrize('x,y,expected,mode', DivisionData.MODE_VALS)
def test_mode_change_x(x, y, expected, mode):
    # Test that with mutable values it still works after x is changed
    dv = DivisionVariants(x)
    assert dv.divide.mode(y, mode) == expected

    dv.x = 0
    assert dv.divide.mode(y, mode) == 0