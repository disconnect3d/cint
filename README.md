## cint: make ctypes great again

This is an attempt to wrap `ctypes.c_*` types so that the arithmetic operators works the same as in C, so:
- value overflow/underflow may occur (yeah, I know that unsigned overflows are UB in C but they _usually_ work)
- when making calculations of two different cint types, the result type will be of bigger or/and unsigned type

**NOTE: This is not production ready, the second goal is not there yet**

#### Example

```
from cint import I32

x = I32(I32.MIN)
assert abs(x) == I32.MIN
assert x-1 == I32.MAX
```
