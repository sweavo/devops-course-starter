# Ask pyflakes not to complain about unused import.
# It's  used, but only by magic.
import pytest  # noqa: F401; pylint: disable=unused-variable

_FIRST = ord("a")
_AFTER = ord("z") + 1
_FIRST_CAP = ord("A")
_AFTER_CAP = ord("Z") + 1


def test_shift_0():
    assert "abczABCZ!" == caesar(0, "abczABCZ!")


def shift_char(shift, c):
    i = ord(c)
    if i >= _FIRST_CAP and i < _AFTER_CAP:
        return shift_char(shift, c.lower()).upper()
    if i >= _FIRST and i < _AFTER:
        return chr(_FIRST + (i - _FIRST + shift) % 26)
    else:
        return c


def test_shiftchar_1():
    assert "b" == shift_char(1, "a")
    assert "a" == shift_char(1, "z")
    assert "B" == shift_char(1, "A")
    assert "A" == shift_char(1, "Z")


def test_shiftchar_neg_1():
    assert "a" == shift_char(-1, "b")
    assert "z" == shift_char(-1, "a")
    assert "A" == shift_char(-1, "B")
    assert "Z" == shift_char(-1, "A")


def test_shiftchar_26():
    for c in "abcdefghijklmnopqrstuvwxxyzABCDEFGHIJKLMNOPQRSTUVWXXYZ!?>":
        assert c == shift_char(26, c)


def caesar(shift, clear):
    return "".join(shift_char(shift, x) for x in clear)


def test_shift_1():
    assert "bcdaBCDA!" == caesar(1, "abczABCZ!")
