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
import math

from cint import I8, U64, F32, F64, SIGNED_INTS, UNSIGNED_INTS, INTS, FLOATS, SIGNED_TYPES, TYPES


@pytest.mark.parametrize('ct', SIGNED_TYPES)
@pytest.mark.parametrize('val', (-1, 0, 1))
def test_abs(ct, val):
    assert abs(ct(val)) == abs(val)


@pytest.mark.parametrize('ct', INTS)
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
def test_ints_overflows_and_underflows(ct):
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
    else:
        assert ct.MIN < 0
    assert ct.MAX > 0


@pytest.mark.parametrize('ct', TYPES)
def test_operators(ct):
    x = 1
    assert x + ct(x) == ct(2 * x) == 2 * x == ct(x) + x


@pytest.mark.parametrize('ct', INTS)
@pytest.mark.parametrize('op', (add, sub, mul, truediv, pow, mod, lshift, rshift, and_, or_, xor))
def test_implicit_casts_when_different_types_are_used_for_ints(ct, op):
    # The U64 is the *strongest* type, so operations with it should always return it
    assert isinstance(op(ct(1), U64(1)), U64)
    assert isinstance(op(U64(1), ct(1)), U64)

    # The I8 is the *weakest* type
    assert isinstance(op(ct(1), I8(1)), ct)
    assert isinstance(op(I8(1), ct(1)), ct)


@pytest.mark.parametrize('ct', TYPES)
@pytest.mark.parametrize('op', (add, sub, mul, truediv, pow))
def test_implicit_casts_when_different_types_are_used_for_all_types(ct, op):
    # Now F64 is the *strongest* type
    assert isinstance(op(ct(1), F64(1)), F64)
    assert isinstance(op(F64(1), ct(1)), F64)

    # The I8 is still the weakest type
    assert isinstance(op(ct(1), I8(1)), ct)
    assert isinstance(op(I8(1), ct(1)), ct)


@pytest.mark.parametrize('ct', INTS)
@pytest.mark.parametrize('op', (add, mul, and_, or_, xor))
def test_alternative_operators_return_the_same_val_for_ints(ct, op):
    left = op(ct(4), 3)
    right = op(3, ct(4))

    assert left == right and left.value == right.value

@pytest.mark.parametrize('ct', TYPES)
@pytest.mark.parametrize('op', (add, mul))
def test_alternative_operators_return_the_same_val_for_all_types(ct, op):
    left = op(ct(4), 3)
    right = op(3, ct(4))

    assert left == right and left.value == right.value


@pytest.mark.parametrize('ct', INTS)
@pytest.mark.parametrize('op', (iadd, isub, imul, ifloordiv, itruediv, ipow, imod, ilshift, irshift, iand, ior, ixor))
def test_inplace_operators_not_returning_other_type_for_ints(ct, op):
    assert isinstance(op(ct(1), U64(1)), ct)

@pytest.mark.parametrize('ct', INTS)
@pytest.mark.parametrize('op', (iadd, isub, imul, ifloordiv, itruediv, ipow))
def test_inplace_operators_not_returning_other_type_for_all_types(ct, op):
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


@pytest.mark.parametrize('ct', TYPES)
@pytest.mark.parametrize('val', [-1, 0, 1])
def test_neg(ct, val):
    left = -ct(val)
    right = ct(-val)
    assert left.value == right.value
    assert left == right


@pytest.mark.parametrize('ct', INTS)
@pytest.mark.parametrize('op', (iadd, isub, imul, ifloordiv, itruediv, ipow, imod, ilshift, irshift, iand, ior, ixor))
def test_not_mutable_ioperators_for_ints(ct, op):
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


@pytest.mark.parametrize('ct', TYPES)
@pytest.mark.parametrize('op', (iadd, isub, imul, ifloordiv, itruediv, ipow))
def test_not_mutable_ioperators_for_all_types(ct, op):
    x = ct(100)
    y = ct(10)

    result = op(x, y)

    expected_result = ct(int(op(100, 10)))
    assert result == expected_result

    assert x == 100
    assert y == 10
    assert id(x) != id(result) != id(y)

@pytest.mark.parametrize('ct', SIGNED_INTS)
def test_invert_signed(ct):
    x = ct(0)
    y = ct(-1)
    inv_x = ~x
    inv_y = ~y
    assert inv_x != x and inv_y != y
    assert inv_x == y
    assert x == inv_y


@pytest.mark.parametrize('ct', UNSIGNED_INTS)
def test_invert_unsigned(ct):
    x = ct(0)
    y = ct.MAX
    inv_x = ~x
    inv_y = ~y
    assert inv_x != x and inv_y != y
    assert inv_x == y
    assert x == inv_y


@pytest.mark.parametrize('ct', FLOATS)
@pytest.mark.parametrize('op', (mod, lshift, rshift, and_, or_, xor, imod, ilshift, irshift, iand, ior, ixor))
def test_invalid_operators_on_floats(ct, op):
    with pytest.raises(TypeError):
        op(ct(1), ct(1))
    with pytest.raises(TypeError):
        op(ct(1), I8(1))    
    with pytest.raises(TypeError):
        op(I8(1), ct(1))

@pytest.mark.parametrize('ct', FLOATS)
def test_int_from_float_conversion(ct):
    x = ct(1.0)
    assert int(x) == 1
    assert ct(int(x)) == x


@pytest.mark.parametrize('ct', FLOATS)
def test_inf_and_nan_values(ct):
    a = ct("inf")
    b = ct("nan")

    assert a == float("inf") and math.isinf(a) and a == a
    assert -a == -float("inf") and math.isinf(-a) and -a == -a
    assert b != b and math.isnan(b)

@pytest.mark.parametrize('ct', FLOATS)
@pytest.mark.parametrize('op', (add, sub, mul, truediv, pow))
def test_inf_and_nan_values_in_operations(ct, op):
    inf = ct("inf")
    nan = ct("nan")
    
    math.isinf(op(inf, 1))
    assert math.isinf(op(inf, 1))
    assert math.isnan(op(nan, 1)) 
    assert math.isnan(op(2, nan))
    assert nan ** 0 == 1 ** nan == 1

    assert math.isnan(op(nan, inf))
    assert math.isnan(op(inf, nan))
    
    assert math.isnan(inf / inf)
    assert math.isnan(inf / -inf)
    assert math.isnan(inf * 0)
    assert math.isnan(inf - inf)

    assert math.isinf(op(inf, inf)) or op in (truediv, sub)
    assert math.isinf(op(inf, -inf)) or op in (truediv, add, pow)
    

# TODO make this functionality available in the library
def _test_binary_representation_of_nan_and_inf():
    # https://en.wikipedia.org/wiki/IEEE_754#Character_representation
    # 9 decimal digits for binary32,
    # 17 decimal digits for binary64
    assert bin(F32('nan')) == "0b01111111110000000000000000000000"
    assert bin(F32('inf')) == "0b01111111100000000000000000000000"

    assert bin(F64('nan')) == "0b0111111111111000000000000000000000000000000000000000000000000000"
    assert bin(F64('inf')) == "0b0111111111110000000000000000000000000000000000000000000000000000"
