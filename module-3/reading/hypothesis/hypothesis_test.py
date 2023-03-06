from hypothesis import given
from hypothesis.strategies import integers


@given(number=integers())
def test_division_with_hypothesis(number):
    assert number / 1 == number
