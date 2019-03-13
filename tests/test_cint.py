from operator import (
    add, sub, mul, truediv, pow, mod, lshift, rshift, and_, or_, xor,
    iadd, isub, imul, itruediv, ipow, imod, ilshift, irshift, iand, ior, ixor
)

# Py2/Py3 compatibility layer
try:
    from operator import ifloordiv
except ImportError:
    from operator import idiv as ifloordiv

import pytest

from cint import I8, U64, SIGNED_INTS, UNSIGNED_INTS, INTS


@pytest.mark.parametrize('ct', SIGNED_INTS)
@pytest.mark.parametrize('val', (-1, 0, 1))
def test_abs(ct, val):
    assert abs(ct(val)) == abs(val)


@pytest.mark.parametrize('ct', SIGNED_INTS)
def test_min_signed_int_mul_minus_one(ct):
    min_ = ct.MIN
    x = ct(min_)

    # MIN * -1
    assert x * -1 == -1 * x == min_
    assert min_ * ct(-1) == ct(-1) * min_ == min_
    assert ct(-1) * x == x * ct(-1) == min_

    # MIN / -1
    assert x / -1 == min_
    assert min_ / ct(-1) == min_
    assert x / ct(-1) == min_

    assert abs(x) == abs(min_) == min_

    # negation with MIN
    assert -x == x


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
    assert x + ct(x) == ct(2 * x) == 2 * x == ct(x) + x


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
@pytest.mark.parametrize('op', (iadd, isub, imul, ifloordiv, itruediv, ipow, imod, ilshift, irshift, iand, ior, ixor))
def test_inplace_operators_not_returning_other_type(ct, op):
    assert isinstance(op(ct(1), U64(1)), ct)


@pytest.mark.parametrize('uint', UNSIGNED_INTS)
def test_signed_vs_unsigned_comparisons(uint):
    """
    cxx is a C++ irc eval bot (see http://www.eelis.net/geordi/)

    <@disconnect3d> cxx << (uint64_t{1} > -1)
    <+cxx> warning: comparison of integer expressions of different signedness:
           'uint64_t' {aka 'long unsigned int'} and 'int'

    # the -w ignores warnings

    <@disconnect3d> cxx -w << (uint64_t{1} > -1)
    <+cxx> false
    """
    val = uint(1)
    assert (val > -1) is False
    assert (val < -1) is True
    assert (val == 1) is True


@pytest.mark.parametrize('ct', INTS)
@pytest.mark.parametrize('val', [-1, 0, 1])
def test_neg(ct, val):
    left = -ct(val)
    right = ct(-val)
    assert left.value == right.value
    assert left == right


@pytest.mark.parametrize('ct', INTS)
@pytest.mark.parametrize('op', (iadd, isub, imul, ifloordiv, itruediv, ipow, imod, ilshift, irshift, iand, ior, ixor))
def test_immutable_min_max(ct, op):
    with pytest.raises(NotImplementedError):
        op(ct.MIN, 1)

    with pytest.raises(NotImplementedError):
        op(ct.MAX, 1)

@pytest.mark.parametrize('ct', INTS)
@pytest.mark.parametrize('op', (iadd, isub, imul, ifloordiv, itruediv, ipow, imod, ilshift, irshift, iand, ior, ixor))
def test_not_mutable_ioperators(ct, op):
    x = ct(100)
    y = ct(10)

    result = op(x, y)

    # Just in case, check the value ;)
    expected_result = ct(int(op(100, 10)))
    assert result == expected_result

    # Check for mutability - the: `x <op>= y` should not modify x
    assert x == 100
    assert y == 10
    assert id(x) != id(result) != id(y)

