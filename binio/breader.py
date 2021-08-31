"""
:mod:`binio.breader` defines the binary stream reader

"""

import io
import struct
import sys
from typing import Optional, Union

from .enums import ByteOrder
from .exceptions import NotEnoughBytes

__all__ = ["BinaryReader"]

# for stupid mypy...
bytes_ = bytes


class BinaryReader:
    """
    A convenient wrapper around a binary stream to read primitive data types.
    """

    def __init__(
        self, b: Union[io.BytesIO, bytes_], byte_order: Optional[ByteOrder] = None
    ) -> None:
        if isinstance(b, bytes_):
            b = io.BytesIO(b)
        elif not isinstance(b, io.BytesIO):
            raise ValueError("Argumnet b must be bytes or io.BytesIO")

        self._stream = b

        if byte_order is None:
            byte_order = ByteOrder.BIG if sys.byteorder == "big" else ByteOrder.LITTLE

        self._byte_order = byte_order
        self._byte_order_fmt = "<" if byte_order == ByteOrder.LITTLE else ">"

    @property
    def stream(self) -> io.BytesIO:
        return self._stream

    @property
    def bytes(self) -> bytes_:
        """
        Return bytes containing the entire contents of the buffer
        of the underlying stream

        :return: bytes
        """
        return self._stream.getvalue()

    @property
    def byte_order(self) -> ByteOrder:
        return self._byte_order

    def _ensure_bytes(self, n: Optional[int] = None) -> bytes_:
        """
        Try to read ``n`` bytes from the underlying storage and
        return them if success.

        :parma n: the required number of bytes. ``None`` means
        consume bytes until EOF is reached.

        :returns: the next portion of bytes. An empty ``bytes`` object
        means that the stream EOF is reached.

        :raises ~binio.exceptions.NotEnoughBytes: if the underlying
        stream contains not enough bytes.

        """
        try:
            b = self._stream.read(n)
        except BlockingIOError as e:
            raise NotEnoughBytes(e) from e

        if n is not None and len(b) < n:
            raise NotEnoughBytes(
                f"Not enough bytes to read. Asked {n} bytes, available {len(b)} bytes."
            )

        return b

    def read_bool(self) -> bool:
        return bool(struct.unpack("?", self._ensure_bytes(1))[0])

    def read_uleb128(self) -> int:
        """
        Read an unsigned LEB128 integer from the underlying
        stream.

        :returns: variable length unsigned integer
        :raises ~binio.exceptions.NotEnoughBytes: if the underlying
        stream contains not enough bytes to unserialize the value of
        the needed type

        """
        v = 0
        offset = 0
        b = 0x80
        while b & 0x80:
            (b,) = self._ensure_bytes(1)
            v |= (b & 0x7F) << offset
            offset += 7

        return v

    def read_zigzagint(self) -> int:
        """
        Read a variable-length signed integer from the underlying
        stream.

        :returns: variable length signed integer
        :raises ~binio.exceptions.NotEnoughBytes: if the underlying
        stream contains not enough bytes to unserialize the value of
        the needed type

        """
        v = self.read_uleb128()
        return (v >> 1) ^ (-(v & 1))

    def read_int8(self) -> int:
        return int(struct.unpack("b", self._ensure_bytes(1))[0])

    def read_uint8(self) -> int:
        return int(struct.unpack("B", self._ensure_bytes(1))[0])

    def read_char(self) -> str:
        return chr(self.read_int8())

    def read_int16(self) -> int:
        return int(struct.unpack(self._byte_order_fmt + "h", self._ensure_bytes(2))[0])

    def read_uint16(self) -> int:
        return int(struct.unpack(self._byte_order_fmt + "H", self._ensure_bytes(2))[0])

    def read_int32(self) -> int:
        return int(struct.unpack(self._byte_order_fmt + "i", self._ensure_bytes(4))[0])

    def read_uint32(self) -> int:
        return int(struct.unpack(self._byte_order_fmt + "I", self._ensure_bytes(4))[0])

    def read_int64(self) -> int:
        return int(struct.unpack(self._byte_order_fmt + "q", self._ensure_bytes(8))[0])

    def read_uint64(self) -> int:
        return int(struct.unpack(self._byte_order_fmt + "Q", self._ensure_bytes(8))[0])

    def read_single(self) -> float:
        return float(
            struct.unpack(self._byte_order_fmt + "f", self._ensure_bytes(4))[0]
        )

    def read_double(self) -> float:
        return float(
            struct.unpack(self._byte_order_fmt + "d", self._ensure_bytes(8))[0]
        )

    def read(self, n: Optional[int] = None) -> bytes_:
        return self._ensure_bytes(n)

    def read_str(self, n: int, encoding: str = "utf-8") -> str:
        return str(
            struct.unpack(str(n) + "s", self._ensure_bytes(n))[0].decode(encoding)
        )

    def read_nullstr(self, encoding: str = "utf-8") -> str:
        s = bytearray()
        while True:
            b = self.read_int8()
            if b == 0x00:
                break
            s.append(b)

        return s.decode(encoding)
