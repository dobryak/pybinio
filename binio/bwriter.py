"""
:mod:`binio.bwriter` defines the binary stream writer

"""

from __future__ import annotations

import io
import struct
import sys
from typing import Optional, Union

from .enums import ByteOrder
from .exceptions import OutOfRange

__all__ = ["BinaryWriter"]

# for stupid mypy...
bytes_ = bytes


class BinaryWriter:
    """
    A convenient wrapper around a binary stream to write primitive data types.
    """

    def __init__(self, byte_order: Optional[ByteOrder]) -> None:
        self._stream = io.BytesIO()
        self._sz = 0

        if byte_order is None:
            byte_order = ByteOrder.BIG if sys.byteorder == "big" else ByteOrder.LITTLE

        self._byte_order = byte_order
        self._byte_order_fmt = "<" if byte_order == ByteOrder.LITTLE else ">"

    @classmethod
    def from_stream(
        cls, stream: io.BytesIO, byte_order: Optional[ByteOrder]
    ) -> BinaryWriter:
        writer = cls(byte_order)
        writer._stream = stream

        return writer

    @property
    def stream(self) -> io.BytesIO:
        return self._stream

    @property
    def bytes(self) -> bytes_:
        return self._stream.getvalue()

    @property
    def size(self) -> int:
        """
        Return the number of bytes written since the
        binary writer was instantiated

        """

        return self._sz

    @property
    def byte_order(self) -> ByteOrder:
        return self._byte_order

    def write_bool(self, b: bool) -> int:
        return self._write_val("?", bool(b))

    def write_uleb128(self, i: int) -> int:
        """
        Write an unsigned LEB128 integer to the underlying
        stream.

        :param i: the unsigned integer to be serialized

        :returns: the number of bytes written to the underlying storage

        :raises: ValueError: if the given value is negative
        :raises: ~binio.exceptions.OutOfRange: if the given value is cannot
        be serialized to the requested format

        """

        if i < 0:
            raise ValueError("An unsigned integer is expected")

        sz = 0
        while i > 0x7F:
            sz += self.write(bytes((i & 0x7F | 0x80,)))
            i >>= 7

        if i > 0:
            sz += self.write(bytes((i,)))

        self._sz += sz
        return sz

    def write_zigzagint(self, i: int) -> int:
        """
        Write a variable-length signed integer to the underlying
        stream using the ZigZag encoding.

        :param i: the signed integer to be serialized

        :returns: the number of bytes written to the underlying storage

        :raises: ~binio.exceptions.OutOfRange: if the given value is cannot
        be serialized to the requested format

        """
        return self.write_uleb128(abs(i) * 2 - (i < 0))

    def write_int8(self, i: int) -> int:
        return self._write_val("b", i)

    def write_uint8(self, i: int) -> int:
        return self._write_val("B", i)

    def write_char(self, c: str) -> int:
        return self.write_int8(ord(c[0]))

    def write_int16(self, i: int) -> int:
        return self._write_val("h", i)

    def write_uint16(self, i: int) -> int:
        return self._write_val("H", i)

    def write_int32(self, i: int) -> int:
        return self._write_val("i", i)

    def write_uint32(self, i: int) -> int:
        return self._write_val("I", i)

    def write_int64(self, i: int) -> int:
        return self._write_val("q", i)

    def write_uint64(self, i: int) -> int:
        return self._write_val("Q", i)

    def write_single(self, f: float) -> int:
        return self._write_val("f", f)

    def write_double(self, d: float) -> int:
        return self._write_val("d", d)

    def write_str(self, s: str, encoding: str = "utf-8") -> int:
        return self.write(s.encode(encoding))

    def write_nullstr(self, s: str, encoding: str = "utf-8") -> int:
        sz = self.write(s.encode(encoding))
        sz += self.write_int8(0)

        return sz

    def _write_val(self, fmt: str, v: Union[int, float]) -> int:
        try:
            b = struct.pack(self._byte_order_fmt + fmt, v)
        except struct.error as e:
            raise OutOfRange(e) from e

        return self.write(b)

    def write(self, b: bytes_) -> int:
        written = 0
        while written < len(b):
            n = self._stream.write(b)
            if n is None:
                raise RuntimeError(
                    "Failed to write given bytes to the underlying stream"
                )

            written += n

        self._sz += written

        return written
