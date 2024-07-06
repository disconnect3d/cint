import ctypes
import ctypes.util
import sys

# Py2/Py3 compatibility layer
# I don't want to depend on e.g. `future` or `six`
# just for this
if sys.version_info.major == 3:
    long = int


def calc(v):
    return getattr(v, 'value', v)


class Cint(object):
    def __init__(self, val):
        if isinstance(val, (int, long, float)):
            super(Cint, self).__init__(val)
        elif isinstance(val, ctypes._SimpleCData):
            super(Cint, self).__init__(val.value)
        elif isinstance(val, str):
            if val.lower() == "nan":
                super(Cint, self).__init__(float('nan'))
            elif val.lower() == "inf":
                super(Cint, self).__init__(float('inf'))
            elif val.lower() == "-inf":
                super(Cint, self).__init__(float('-inf'))
        else:
            raise ValueError("Wrong value passed to __init__")

    # Methods from ctypes._CData - we override them so that they are visible in `dir(obj)`
    # in theory we could just override  `__dir__` but that wouldn't show up them in `dir(cint_type)`
    # a good thing about it is that we can make better docs
    @classmethod
    def from_buffer(cls, source, offset=0):
        """
        Creates a Cint instance from a writeable `source` buffer.

        Note that the resulting object will just hold a pointer to the buffer
        and *it does not manage the lifetime of that buffer* so you must explicitly
        make sure that it doesn't go out of scope or you will end up with undefined behavior.
        """
        return cls.from_buffer(source, offset)


    @classmethod
    def from_buffer_copy(cls, source, offset=0):
        """
        Creates a Cint instance from a readable `source` buffer.

        The buffer object is copied and managed by the Cint instance.
        """
        return cls.from_buffer_copy(source, offset)

    @classmethod
    def from_address(cls, address):
        """
        Creates a Cint instance from a given `address` (integer).

        Note that the resulting object won't manage the lifetime of the underlying memory.
        See also docs for `from_buffer`.
        """
        return cls.from_address(address)

    # Cint details below
    @classmethod
    def __stronger_type(cls, other):
        if isinstance(other, (int, long, float)):
            return cls
        elif not isinstance(other, (INTS, FLOATS)):
            raise ValueError("Cannot perform arithmetic operations between %s and %s" % (cls, type(other)))

        other = other.__class__

        # FLOATS are *stronger* than INTS
        if (cls in INTS and other in FLOATS) or (cls in FLOATS and other in INTS):
            return other if cls in INTS else cls

        
        return cls if (cls.SIZE, cls.UNSIGNED) > (other.SIZE, other.UNSIGNED) else other

    if sys.version_info.major == 2:
        def __coerce__(self, other):
            return (self, self.__stronger_type(other)(calc(other)))

    def __add__(self, other):
        return self.__stronger_type(other)(self.value + calc(other))

    __radd__ = __add__

    def __sub__(self, other):
        return self.__stronger_type(other)(self.value - calc(other))

    def __rsub__(self, other):
        return self.__stronger_type(other)(calc(other) - self.value)

    def __mul__(self, other):
        return self.__stronger_type(other)(self.value * calc(other))

    __rmul__ = __mul__

    def __pow__(self, other):
        return self.__stronger_type(other)(self.value ** calc(other))

    def __rpow__(self, other):
        return self.__stronger_type(other)(calc(other) ** self.value)

    def __truediv__(self, other):
        return self.__stronger_type(other)(self.value // calc(other))

    # __div__ is Python 2 only
    __div__ = __floordiv__ = __truediv__

    def __rtruediv__(self, other):
        return self.__stronger_type(other)(calc(other) // self.value)

    # __rdiv__ is Python 2 only
    __rdiv__ = __rfloordiv__ = __rtruediv__

    def __mod__(self, other):
        if isinstance(other, (float, F32, F64)) or isinstance(self.value, (float, F32, F64)):
            raise TypeError(f"unsupported operand type(s) for %: {self.__class__.__name__} and 'float'")
        return self.__stronger_type(other)(self.value % calc(other))

    def __rmod__(self, other):
        return self.__stronger_type(other)(calc(other) % self.value)

    def __eq__(self, other):
        return self.value == calc(other)

    def __gt__(self, other):
        return self.value > self.__stronger_type(other)(other).value

    def __lt__(self, other):
        return self.value < self.__stronger_type(other)(other).value

    def __ge__(self, other):
        return self.value >= self.__stronger_type(other)(other).value

    def __le__(self, other):
        return self.value <= self.__stronger_type(other)(other).value

    def __lshift__(self, other):
        return self.__stronger_type(other)(self.value << calc(other))

    def __rlshift__(self, other):
        return self.__stronger_type(other)(calc(other) << self.value)

    def __rshift__(self, other):
        return self.__stronger_type(other)(self.value >> calc(other))

    def __rrshift__(self, other):
        return self.__stronger_type(other)(calc(other) >> self.value)

    def __and__(self, other):
        return self.__stronger_type(other)(self.value & calc(other))

    def __rand__(self, other):
        return self.__stronger_type(other)(calc(other) & self.value)

    def __or__(self, other):
        return self.__stronger_type(other)(self.value | calc(other))

    def __ror__(self, other):
        return self.__stronger_type(other)(calc(other) | self.value)

    def __xor__(self, other):
        return self.__stronger_type(other)(self.value ^ calc(other))

    def __rxor__(self, other):
        return self.__stronger_type(other)(calc(other) ^ self.value)

    def __bool__(self):
        return self.value != 0

    def __hash__(self):
        # returning `hash(self.value)` would be **bug prone**
        # (imagine if the object would be stored in a collection and then mutated)
        return id(self)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.value)

    def __iadd__(self, other):
        return self.__class__(self.value + calc(other))

    def __isub__(self, other):
        return self.__class__(self.value - calc(other))

    def __imul__(self, other):
        return self.__class__(self.value * calc(other))

    def __ipow__(self, other):
        return self.__class__(self.value ** calc(other))

    def __itruediv__(self, other):
        return self.__class__(self.value // calc(other))

    # __idiv__ is Python 2 only
    __idiv__ = __ifloordiv__ = __itruediv__

    def __imod__(self, other):
        if isinstance(other, (float, F32, F64)) or isinstance(self.value, (float, F32, F64)):
            raise TypeError(f"unsupported operand type(s) for %=: {self.__class__.__name__} and 'float'")
        return self.__class__(self.value % calc(other))

    def __irshift__(self, other):
        return self.__class__(self.value >> calc(other))

    def __ilshift__(self, other):
        return self.__class__(self.value << calc(other))

    def __ixor__(self, other):
        return self.__class__(self.value ^ calc(other))

    def __iand__(self, other):
        return self.__class__(self.value & calc(other))

    def __ior__(self, other):
        return self.__class__(self.value | calc(other))

    def __neg__(self):
        return self.__class__(-self.value)

    def __pos__(self):
        return self.__class__(self.value)

    def __abs__(self):
        return self.__class__(abs(self.value))

    def __invert__(self):
        return self.__class__(~self.value)

    def __complex__(self):
        return complex(self.value)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    __index__ = __int__  # make indexing work




class I8(Cint, ctypes.c_int8):
    MIN = -2 ** 7
    MAX = 2 ** 7 - 1
    UNSIGNED = False
    CTYPEDEF = 'int8_t'
    SIZE = 1


class I16(Cint, ctypes.c_int16):
    MIN = -2 ** 15
    MAX = 2 ** 15 - 1
    UNSIGNED = False
    CTYPEDEF = 'int16_t'
    SIZE = 2


class I32(Cint, ctypes.c_int32):
    MIN = -2 ** 31
    MAX = 2 ** 31 - 1
    UNSIGNED = False
    CTYPEDEF = 'int32_t'
    SIZE = 4


class I64(Cint, ctypes.c_int64):
    MIN = -2 ** 63
    MAX = 2 ** 63 - 1
    UNSIGNED = False
    CTYPEDEF = 'int64_t'
    SIZE = 8


class U8(Cint, ctypes.c_uint8):
    MIN = 0
    MAX = 2 ** 8 - 1
    UNSIGNED = True
    CTYPEDEF = 'uint8_t'
    SIZE = 1


class U16(Cint, ctypes.c_uint16):
    MIN = 0
    MAX = 2 ** 16 - 1
    UNSIGNED = True
    CTYPEDEF = 'uint16_t'
    SIZE = 2


class U32(Cint, ctypes.c_uint32):
    MIN = 0
    MAX = 2 ** 32 - 1
    UNSIGNED = True
    CTYPEDEF = 'uint32_t'
    SIZE = 4


class U64(Cint, ctypes.c_uint64):
    MIN = 0
    MAX = 2 ** 64 - 1
    UNSIGNED = True
    CTYPEDEF = 'uint64_t'
    SIZE = 8


class F32(Cint, ctypes.c_float):
    # MIN/MAX are not defined for floats
    # Update: well, maybe they are definded after all
    MIN = 2 ** -126
    MAX = (2 - 2 ** -23) * 2 ** 127
    UNSIGNED = False
    CTYPEDEF = 'float'
    SIZE = 4    

class F64(Cint, ctypes.c_double):
    MIN = 2 ** -1022
    MAX = (2 - 2 ** -52) * 2 ** 1023
    UNSIGNED = False
    CTYPEDEF = 'double'
    SIZE = 8

SIGNED_INTS = (I8, I16, I32, I64)
UNSIGNED_INTS = (U8, U16, U32, U64)

FLOATS = (F32, F64)

INTS = SIGNED_INTS + UNSIGNED_INTS
SIGNED_TYPES = SIGNED_INTS + FLOATS
TYPES = INTS + FLOATS

# fix MIN/MAX values to have proper type
for _type in TYPES:
    _type.MIN = _type(_type.MIN)
    _type.MAX = _type(_type.MAX)
