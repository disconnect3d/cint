[![Build Status](https://travis-ci.com/disconnect3d/cint.svg?branch=master)](https://travis-ci.com/disconnect3d/cint)
## cint: make ctypes great again

This is a wrapper for `ctypes.c_*` types so that the arithmetic operators works the same as in C, so:
- value overflow/underflow may occur (yeah, I know that unsigned overflows are UB in C but they _usually_ work)
- when making calculations of two different cint types, the result type will be of bigger or/and unsigned type

**Install with `pip install cint`! Supports both Python 2 and Python 3.**

### Examples

```python
from cint import I8, I32, U64, Cint

def rand_gen(seed):
    """Returns a rng that generates numbers in a range of given cint type"""
    assert isinstance(seed, Cint)

    while True:
        seed = 1103515245 * seed + 12345
        yield seed

# a simple I32 range rand
rand_i32 = rand_gen(I32(1))
rand_u64 = rand_gen(U64(2))

for i in range(10):
    print("Gen %d number: i32 = %d, u64 = %d" % (next(rand_i32()), next(rand_u64())))

# We can do simple overflows
print("I8(127) + 1 = %d" % (I8(127) + 1))

# Some other 'weird' cases are also handled - see tests for more! ;)
print("-1 * I8(-128) = %d" % (-1 * I8(-128)))
print("abs(I32.MIN) = %d" % abs(I32.MIN))

# Adding numbers of two different types will result in bigger type result
x = I32(1) + U64(2)
print("x = %r" % x)  # U64(3)

# There are also .MIN and .MAX constants
print("U64 min value = %d, max value = %d" % (U64.MIN, U64.MAX))
```

### Why this lib?

Sometimes you just need the old, low level behavior of int/unsigned types. This may be handy during reverse engineering and rewritting some C code to Python.
