import ctypes
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
        if isinstance(val, (int, long)):
            super(Cint, self).__init__(val)
        elif isinstance(val, ctypes._SimpleCData):
            super(Cint, self).__init__(val.value)
        else:
            raise ValueError("Wrong value passed to __init__")

    @classmethod
    def __stronger_type(cls, other):
        if isinstance(other, (int, long)):
            return cls
        elif not isinstance(other, INTS):
            raise ValueError("Cannot perform arithmetic operations between %s and %s" % (cls, type(other)))

        other = other.__class__

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

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __bool__(self):
        return self.value != 0

    def __abs__(self):
        return self.__class__(abs(self.value))

    def __neg__(self):
        return self.__class__(-self.value)

    def __hash__(self):
        # returning `hash(self.value)` would be **bug prone**
        # (imagine if the object would be stored in a collection and then mutated)
        return id(self)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.value)

    __index__ = __int__  # make indexing work

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


class ImmutableCint(object):
    pass

def create_immutable(val, type_):
    class ImmutableCintX(type_, ImmutableCint):
        def __not_implemented__(self, _):
            raise NotImplementedError

        __iadd__ = __not_implemented__
        __isub__ = __not_implemented__
        __imul__ = __not_implemented__
        __ipow__ = __not_implemented__
        __itruediv__ = __not_implemented__
        __ifloordiv__ = __not_implemented__
        __idiv__ = __not_implemented__  # Python 2 only
        __imod__ = __not_implemented__
        __irshift__ = __not_implemented__
        __ilshift__ = __not_implemented__
        __ior__ = __not_implemented__
        __iand__ = __not_implemented__
        __ixor__ = __not_implemented__

    return ImmutableCintX(val)


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


SIGNED_INTS = (I8, I16, I32, I64)
UNSIGNED_INTS = (U8, U16, U32, U64)

INTS = SIGNED_INTS + UNSIGNED_INTS

# fix/pin MIN/MAX values to be immutable (i.e. can't do U8.MIN += 2)
for _type in INTS:
    _type.MIN = create_immutable(_type.MIN, _type)
    _type.MAX = create_immutable(_type.MAX, _type)
