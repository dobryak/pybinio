# PyBinIO

**PyBinIO** - is a wrapper around the `struct` python module. It contains
convenient reader and writer classes that can be used to write primitive data
types in a specific byte order.  

In addition it supports:
- [LEB128](https://en.wikipedia.org/wiki/LEB128) for encoding **unsigned**
  variable length integers.  
- [Zigzag](https://en.wikipedia.org/wiki/Variable-length_quantity#Zigzag_encoding)
  for encoding **signed** variable length integers.  

## Install

The package is available on PyPI.

```console
$ python3 -m pip install pybinio

```

## Usage

```python
import binio

value = 255
writer = binio.BinaryWriter(binio.ByteOrder.LITTLE)
writer.write_uint8(value)

reader = binio.BinaryReader(writer.bytes, binio.ByteOrder.LITTLE)
assert value == reader.read_uint8()

```
