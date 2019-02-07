import ctypes
from struct import calcsize


def calc(v):
    return getattr(v, 'value', v)


def gen_int_type(name: str, ctype: ctypes._SimpleCData) -> object:
    """
    Generates a ctype type wrapper for (u)int8/16/32/64 types.
    """
    unsigned = ctype.__name__.startswith('c_u')

    size_bytes = calcsize(ctype._type_)
    bits = size_bytes * 8

    class Type(ctype):
        """
        ctypes.c_[u]intXX wrapper that adds C-like operators/value semantics so:
        - overflow and underflow of the value may happen
        - when calculated among a bigger or/and unsigned type, returns it

        It also adds certain useful static attributes such as:
        - MIN - minimum possible value
        - MAX - maximum possible value
        - CTYPEDEF - C-like cross platform typedef (e.g. 'uint32_t')
        - SIGNED - True/False whether the type is signed or unsigned
        - SIZE - size in bytes
        """
        if unsigned:
            MIN = 0
            MAX = 2 ** bits - 1
        else:
            MIN = -2 ** (bits-1)
            MAX = 2 ** (bits-1) - 1

        CTYPEDEF = ('uint{}_t' if unsigned else 'int{}_t').format(bits)
        SIGNED = not unsigned
        SIZE = size_bytes

        __qualname__ = name

        def __add__(self, other):
            return Type(ctype(self.value + calc(other)).value)

        def __iadd__(self, other):
            self.value += calc(other)
            return self

        __radd__ = __add__

        def __sub__(self, other):
            return Type(ctype(self.value - calc(other)).value)

        def __rsub__(self, other):
            return Type(calc(other) - self.value)

        def __isub__(self, other):
            self.value -= calc(other)
            return self

        def __mul__(self, other):
            return Type(ctype(self.value * calc(other)).value)

        __rmul__ = __mul__

        def __imul__(self, other):
            self.value *= calc(other)
            return self

        def __pow__(self, other):
            return Type(ctype(self.value ** calc(other)).value)

        def __rpow__(self, other):
            return Type(calc(other) ** self.value)

        def __ipow__(self, other):
            self.value **= calc(other)
            return self

        def __truediv__(self, other):
            return Type(ctype(self.value // calc(other)).value)

        def __rtruediv__(self, other):
            return Type(calc(other) // self.value)

        def __idiv__(self, other):
            self.value //= calc(other)
            return self

        def __mod__(self, other):
            return Type(self.value % calc(other))

        def __rmod__(self, other):
            return Type(calc(other) % self.value)

        def __imod__(self, other):
            self.value %= calc(other)
            return self

        def __eq__(self, other):
            return self.value == calc(other)

        def __gt__(self, other):
            return self.value > calc(other)

        def __lt__(self, other):
            return self.value < calc(other)

        def __ge__(self, other):
            return self.value >= calc(other)

        def __le__(self, other):
            return self.value <= calc(other)

        def __lshift__(self, other):
            return Type(self.value << calc(other))

        def __rlshift__(self, other):
            return Type(calc(other) << self.value)

        def __ilshift__(self, other):
            self.value <<= calc(other)
            return self

        def __rshift__(self, other):
            return Type(self.value >> calc(other))

        def __rrshift__(self, other):
            return Type(calc(other) >> self.value)

        def __irshift__(self, other):
            self.value >>= calc(other)
            return self

        def __and__(self, other):
            return Type(self.value & calc(other))

        def __rand__(self, other):
            return Type(calc(other) & self.value)

        def __iand__(self, other):
            self.value &= calc(other)
            return self

        def __or__(self, other):
            return Type(self.value | calc(other))

        def __ror__(self, other):
            return Type(calc(other) | self.value)

        def __ior__(self, other):
            self.value |= calc(other)
            return self

        def __xor__(self, other):
            return Type(self.value ^ calc(other))

        def __rxor__(self, other):
            return Type(calc(other) ^ self.value)

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
            return Type(abs(self.value))

        def __neg__(self):
            return Type(-self.value)

        def __hash__(self):
            # returning `hash(self.value)` would be **bug prone**
            # (imagine if the object would be stored in a collection and then mutated)
            return id(self)

        def __str__(self):
            return str(self.value)

        def __repr__(self):
            return '{}({})'.format(self.__class__.__name__, self.value)

        __index__ = __int__  # make indexing work

    return Type


I8 = gen_int_type('I8', ctypes.c_int8)
I16 = gen_int_type('I16', ctypes.c_int16)
I32 = gen_int_type('I32', ctypes.c_int32)
I64 = gen_int_type('I64', ctypes.c_int64)

U8 = gen_int_type('U8', ctypes.c_uint8)
U16 = gen_int_type('U16', ctypes.c_uint16)
U32 = gen_int_type('U32', ctypes.c_uint32)
U64 = gen_int_type('U64', ctypes.c_uint64)
