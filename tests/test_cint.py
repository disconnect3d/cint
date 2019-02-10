import pytest
from cint import I8, I16, I32, I64, U8, U16, U32, U64, SIGNED_INTS, INTS
from operator import (
    add, sub, mul, truediv, pow, mod, lshift, rshift, and_, or_, xor,
    iadd, isub, imul, itruediv, ipow, imod, ilshift, irshift, iand, ior, ixor
)


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

    if ct.UNSIGNED:
        assert ct.MIN == 0


@pytest.mark.parametrize('ct', INTS)
def test_operators(ct):
    x = 1
    assert x + ct(x) == ct(2*x) == 2*x == ct(x) + x


@pytest.mark.parametrize('ct', INTS)
@pytest.mark.parametrize('op', (add, sub, mul, truediv, pow, mod, lshift, rshift, and_, or_, xor))
def test_implicit_casts_when_different_types_are_used(ct, op):
    # The U64 is the *strongest* type, so operations with it should always return it
    assert isinstance(op(ct(1), U64(1)), U64)
    assert isinstance(op(U64(1), ct(1)), U64)

    # The I8 is the *weakest* type
    assert isinstance(op(ct(1), I8(1)), ct)
    assert isinstance(op(I8(1), ct(1)), ct)


@pytest.mark.parametrize('ct', INTS)
@pytest.mark.parametrize('op', (add, mul, and_, or_, xor))
def test_alternative_operators_return_the_same_val(ct, op):
    left = op(ct(4), 3)
    right = op(3, ct(4))

    assert left == right and left.value == right.value


@pytest.mark.parametrize('ct', INTS)
@pytest.mark.parametrize('op', (iadd, isub, imul, itruediv, ipow, imod, ilshift, irshift, iand, ior, ixor))
def test_inplace_operators_not_returning_other_type(ct, op):
    assert isinstance(op(ct(1), U64(1)), ct)
