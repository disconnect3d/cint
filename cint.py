import ctypes


def calc(v):
    return getattr(v, 'value', v)


class WrappedCint:
    def __init__(self, val):
        if isinstance(val, int):
            super().__init__(val)
        elif isinstance(val, ctypes._SimpleCData):
            super().__init__(val.value)
        else:
            raise ValueError("Wrong value passed to __init__")

    @classmethod
    def __stronger_type(cls, other):
        if isinstance(other, int):
            return cls
        elif not isinstance(other, INTS):
            raise ValueError("Cannot perform arithmetic operations between %s and %s" % (cls, type(other)))

        other = other.__class__

        return cls if (cls.SIZE, cls.UNSIGNED) > (other.SIZE, other.UNSIGNED) else other

    def __add__(self, other):
        return self.__stronger_type(other)(self.value + calc(other))

    def __iadd__(self, other):
        self.value += calc(other)
        return self

    __radd__ = __add__

    def __sub__(self, other):
        return self.__stronger_type(other)(self.value - calc(other))

    def __rsub__(self, other):
        return self.__stronger_type(other)(calc(other) - self.value)

    def __isub__(self, other):
        self.value -= calc(other)
        return self

    def __mul__(self, other):
        return self.__stronger_type(other)(self.value * calc(other))

    __rmul__ = __mul__

    def __imul__(self, other):
        self.value *= calc(other)
        return self

    def __pow__(self, other):
        return self.__stronger_type(other)(self.value ** calc(other))

    def __rpow__(self, other):
        return self.__stronger_type(other)(calc(other) ** self.value)

    def __ipow__(self, other):
        self.value **= calc(other)
        return self

    def __truediv__(self, other):
        return self.__stronger_type(other)(self.value // calc(other))

    def __rtruediv__(self, other):
        return self.__stronger_type(other)(calc(other) // self.value)

    def __itruediv__(self, other):
        self.value //= calc(other)
        return self

    def __mod__(self, other):
        return self.__stronger_type(other)(self.value % calc(other))

    def __rmod__(self, other):
        return self.__stronger_type(other)(calc(other) % self.value)

    def __imod__(self, other):
        self.value %= calc(other)
        return self

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

    def __ilshift__(self, other):
        self.value <<= calc(other)
        return self

    def __rshift__(self, other):
        return self.__stronger_type(other)(self.value >> calc(other))

    def __rrshift__(self, other):
        return self.__stronger_type(other)(calc(other) >> self.value)

    def __irshift__(self, other):
        self.value >>= calc(other)
        return self

    def __and__(self, other):
        return self.__stronger_type(other)(self.value & calc(other))

    def __rand__(self, other):
        return self.__stronger_type(other)(calc(other) & self.value)

    def __iand__(self, other):
        self.value &= calc(other)
        return self

    def __or__(self, other):
        return self.__stronger_type(other)(self.value | calc(other))

    def __ror__(self, other):
        return self.__stronger_type(other)(calc(other) | self.value)

    def __ior__(self, other):
        self.value |= calc(other)
        return self

    def __xor__(self, other):
        return self.__stronger_type(other)(self.value ^ calc(other))

    def __rxor__(self, other):
        return self.__stronger_type(other)(calc(other) ^ self.value)

    def __ixor__(self, other):
        self.value ^= calc(other)
        return self

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


class I8(WrappedCint, ctypes.c_int8):
    MIN = -2 ** 7
    MAX = 2 ** 7 - 1
    UNSIGNED = False
    CTYPEDEF = 'int8_t'
    SIZE = 1


class I16(WrappedCint, ctypes.c_int16):
    MIN = -2 ** 15
    MAX = 2 ** 15 - 1
    UNSIGNED = False
    CTYPEDEF = 'int16_t'
    SIZE = 2


class I32(WrappedCint, ctypes.c_int32):
    MIN = -2 ** 31
    MAX = 2 ** 31 - 1
    UNSIGNED = False
    CTYPEDEF = 'int32_t'
    SIZE = 4


class I64(WrappedCint, ctypes.c_int64):
    MIN = -2 ** 63
    MAX = 2 ** 63 - 1
    UNSIGNED = False
    CTYPEDEF = 'int64_t'
    SIZE = 8


class U8(WrappedCint, ctypes.c_uint8):
    MIN = 0
    MAX = 2 ** 8 - 1
    UNSIGNED = True
    CTYPEDEF = 'uint8_t'
    SIZE = 1


class U16(WrappedCint, ctypes.c_uint16):
    MIN = 0
    MAX = 2 ** 16 - 1
    UNSIGNED = True
    CTYPEDEF = 'uint16_t'
    SIZE = 2


class U32(WrappedCint, ctypes.c_uint32):
    MIN = 0
    MAX = 2 ** 32 - 1
    UNSIGNED = True
    CTYPEDEF = 'uint32_t'
    SIZE = 4


class U64(WrappedCint, ctypes.c_uint64):
    MIN = 0
    MAX = 2 ** 64 - 1
    UNSIGNED = True
    CTYPEDEF = 'uint64_t'
    SIZE = 8


SIGNED_INTS = (I8, I16, I32, I64)
UNSIGNED_INTS = (U8, U16, U32, U64)

INTS = SIGNED_INTS + UNSIGNED_INTS
