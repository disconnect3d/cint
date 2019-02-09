import ctypes
from struct import calcsize


def calc(v):
    return getattr(v, 'value', v)


class WrappedCintMeta(type):
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
    def __new__(cls, cls_name, bases, cls_data):
        """
        :param cls_name: Name of instantiated class (must be in I8/16/32/64 or U8/16/32/64)
        :param bases: Tuple of base classes
        :param cls_data: All attributes defined on a class
        """
        assert cls_name[0] in 'IU'
        assert int(cls_name[1:]) in (8, 16, 32, 64)

        signed = cls_name[0] == 'I'
        bits = int(cls_name[1:])

        if signed:
            cls_data['MIN'] = -2 ** (bits - 1)
            cls_data['MAX'] = 2 ** (bits - 1) - 1
        else:
            cls_data['MIN'] = 0
            cls_data['MAX'] = 2 ** bits - 1

        # retrieve the ctypes' type and put it as a base class
        typename = 'int' if signed else 'uint'
        typename += str(bits)
        ctype = getattr(ctypes, 'c_' + typename)

        cls_data['CTYPEDEF'] = ('int{}_t' if signed else 'uint{}_t').format(bits)
        cls_data['SIGNED'] = signed
        cls_data['SIZE'] = bits/8

        cls_data['ctype'] = ctype  # TODO / FIXME - remove it
        bases = bases + (ctype,)

        # Note that we do not pass `cls` here and `type`
        # This is because we want the class to inherit from ctypes types
        # And they don't play well if we use  `metaclass=...`
        return super().__new__(type, cls_name, bases, cls_data)


class WrappedCint:
    def __init__(self, val):
        if isinstance(val, int):
            super().__init__(val)
        elif isinstance(val, ctypes._SimpleCData):
            super().__init__(val.value)
        else:
            raise ValueError("Wrong value passed to __init__")

    def __add__(self, other):
        return self.__class__(self.ctype(self.value + calc(other)).value)

    def __iadd__(self, other):
        self.value += calc(other)
        return self

    __radd__ = __add__

    def __sub__(self, other):
        return self.__class__(self.ctype(self.value - calc(other)).value)

    def __rsub__(self, other):
        return self.__class__(calc(other) - self.value)

    def __isub__(self, other):
        self.value -= calc(other)
        return self

    def __mul__(self, other):
        return self.__class__(self.ctype(self.value * calc(other)).value)

    __rmul__ = __mul__

    def __imul__(self, other):
        self.value *= calc(other)
        return self

    def __pow__(self, other):
        return self.__class__(self.ctype(self.value ** calc(other)).value)

    def __rpow__(self, other):
        return self.__class__(calc(other) ** self.value)

    def __ipow__(self, other):
        self.value **= calc(other)
        return self

    def __truediv__(self, other):
        return self.__class__(self.ctype(self.value // calc(other)).value)

    def __rtruediv__(self, other):
        return self.__class__(calc(other) // self.value)

    def __idiv__(self, other):
        self.value //= calc(other)
        return self

    def __mod__(self, other):
        return self.__class__(self.value % calc(other))

    def __rmod__(self, other):
        return self.__class__(calc(other) % self.value)

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
        return self.__class__(self.value << calc(other))

    def __rlshift__(self, other):
        return self.__class__(calc(other) << self.value)

    def __ilshift__(self, other):
        self.value <<= calc(other)
        return self

    def __rshift__(self, other):
        return self.__class__(self.value >> calc(other))

    def __rrshift__(self, other):
        return self.__class__(calc(other) >> self.value)

    def __irshift__(self, other):
        self.value >>= calc(other)
        return self

    def __and__(self, other):
        return self.__class__(self.value & calc(other))

    def __rand__(self, other):
        return self.__class__(calc(other) & self.value)

    def __iand__(self, other):
        self.value &= calc(other)
        return self

    def __or__(self, other):
        return self.__class__(self.value | calc(other))

    def __ror__(self, other):
        return self.__class__(calc(other) | self.value)

    def __ior__(self, other):
        self.value |= calc(other)
        return self

    def __xor__(self, other):
        return self.__class__(self.value ^ calc(other))

    def __rxor__(self, other):
        return self.__class__(calc(other) ^ self.value)

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


class I8(WrappedCint, metaclass=WrappedCintMeta):
    pass


class I16(WrappedCint, metaclass=WrappedCintMeta):
    pass


class I32(WrappedCint, metaclass=WrappedCintMeta):
    pass


class I64(WrappedCint, metaclass=WrappedCintMeta):
    pass


class U8(WrappedCint, metaclass=WrappedCintMeta):
    pass


class U16(WrappedCint, metaclass=WrappedCintMeta):
    pass


class U32(WrappedCint, metaclass=WrappedCintMeta):
    pass


class U64(WrappedCint, metaclass=WrappedCintMeta):
    pass
