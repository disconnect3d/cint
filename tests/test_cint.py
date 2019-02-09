import pytest
from cint import I8, I16, I32, I64, U8, U16, U32, U64, SIGNED_INTS, UNSIGNED_INTS, INTS


@pytest.mark.parametrize('ct', SIGNED_INTS)
@pytest.mark.parametrize('val', (-1, 0, 1))
def test_abs(ct, val):
    assert abs(ct(val)) == abs(val)


@pytest.mark.parametrize('ct', SIGNED_INTS)
def test_signed_minimum_value_arithmetics(ct):
    min_ = ct.MIN

    # MIN * -1
    assert ct(min_) * -1 == -1 * ct(min_) == min_
    assert min_ * ct(-1) == ct(-1) * min_ == min_
    assert ct(-1) * ct(min_) == ct(min_) * ct(-1) == min_

    # MIN / -1
    assert  ct(min_) / -1 == min_
    assert min_ / ct(-1) == min_
    assert ct(min_) / ct(-1) == min_

    # since ct.MIN is a Python int, the last abs returns a positive number
    assert abs(ct(min_)) == min_ != abs(min_)


@pytest.mark.parametrize('ct', INTS)
def test_overflows_and_underflows(ct):
    min_ = ct.MIN
    max_ = ct.MAX

    assert ct(min_) - 1 == max_
    assert min_ - ct(1) == max_
    assert ct(min_) - ct(1) == max_

    assert ct(max_) + 1 == min_
    assert max_ + ct(1) == min_
    assert ct(max_) + ct(1) == min_


@pytest.mark.parametrize('ct', INTS)
def test_operators(ct):
    x = 1
    assert x + ct(x) == ct(2*x) == 2*x == ct(x) + x

