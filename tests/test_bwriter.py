import io
import unittest

from binio import BinaryWriter, ByteOrder


class BinaryWriterTests(unittest.TestCase):
    def test_size(self) -> None:
        writer = BinaryWriter(ByteOrder.LITTLE)

        self.assertEqual(writer.size, 0)
        writer.write_uint8(255)
        self.assertEqual(writer.size, 1)
        writer.write_int16(3456)
        self.assertEqual(writer.size, 3)

    def test_uleb128(self) -> None:
        writer = BinaryWriter(ByteOrder.LITTLE)

        writer.write_uleb128(300)
        self.assertEqual(writer.bytes, b"\xac\x02")
        writer.write_uleb128(255)
        self.assertEqual(writer.bytes, b"\xac\x02\xff\x01")

        writer = BinaryWriter(ByteOrder.LITTLE)

        writer.write_uleb128(18446744073709551615)
        self.assertEqual(writer.bytes, b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01")

    def test_from_stream(self) -> None:
        stream = io.BytesIO()
        writer = BinaryWriter.from_stream(stream, ByteOrder.LITTLE)

        writer.write_uleb128(300)

        self.assertEqual(stream.getvalue(), b"\xac\x02")

    def test_get_stream(self) -> None:
        stream = io.BytesIO()
        writer = BinaryWriter.from_stream(stream, ByteOrder.LITTLE)

        self.assertEqual(stream, writer.stream)

    def test_zigzagint(self) -> None:
        writer = BinaryWriter(ByteOrder.LITTLE)

        writer.write_zigzagint(-5)
        self.assertEqual(writer.bytes, b"\x09")

        writer.write_zigzagint(5)
        self.assertEqual(writer.bytes, b"\x09\x0a")

        writer.write_zigzagint(-345)
        self.assertEqual(writer.bytes, b"\x09\x0a\xb1\x05")

    def test_int8(self) -> None:
        writer = BinaryWriter(ByteOrder.LITTLE)

        writer.write_int8(1)
        self.assertEqual(writer.bytes, b"\x01")
        writer.write_int8(127)
        self.assertEqual(writer.bytes, b"\x01\x7f")
        writer.write_int8(-128)
        self.assertEqual(writer.bytes, b"\x01\x7f\x80")

    def test_uint8(self) -> None:
        writer = BinaryWriter(ByteOrder.LITTLE)

        writer.write_uint8(255)
        self.assertEqual(writer.bytes, b"\xff")
        writer.write_uint8(0)
        self.assertEqual(writer.bytes, b"\xff\x00")
        writer.write_uint8(128)
        self.assertEqual(writer.bytes, b"\xff\x00\x80")

    def test_int16(self) -> None:
        writer = BinaryWriter(ByteOrder.LITTLE)

        writer.write_int16(1)
        self.assertEqual(writer.bytes, b"\x01\x00")
        writer.write_int16(-1)
        self.assertEqual(writer.bytes, b"\x01\x00\xff\xff")
        writer.write_int16(-32768)
        self.assertEqual(writer.bytes, b"\x01\x00\xff\xff\x00\x80")

    def test_uint16(self) -> None:
        writer = BinaryWriter(ByteOrder.LITTLE)

        writer.write_uint16(1)
        self.assertEqual(writer.bytes, b"\x01\x00")
        writer.write_uint16(65535)
        self.assertEqual(writer.bytes, b"\x01\x00\xff\xff")
        writer.write_uint16(32768)
        self.assertEqual(writer.bytes, b"\x01\x00\xff\xff\x00\x80")

    def test_int32(self) -> None:
        writer = BinaryWriter(ByteOrder.LITTLE)

        writer.write_int32(1)
        self.assertEqual(writer.bytes, b"\x01\x00\x00\x00")
        writer.write_int32(-1)
        self.assertEqual(writer.bytes, b"\x01\x00\x00\x00\xff\xff\xff\xff")
        writer.write_int32(-2147483648)
        self.assertEqual(
            writer.bytes, b"\x01\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x80"
        )

    def test_uint32(self) -> None:
        writer = BinaryWriter(ByteOrder.LITTLE)

        writer.write_uint32(1)
        self.assertEqual(writer.bytes, b"\x01\x00\x00\x00")
        writer.write_uint32(4294967295)
        self.assertEqual(writer.bytes, b"\x01\x00\x00\x00\xff\xff\xff\xff")
        writer.write_uint32(2147483648)
        self.assertEqual(
            writer.bytes, b"\x01\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x80"
        )

    def test_int64(self) -> None:
        writer = BinaryWriter(ByteOrder.LITTLE)

        writer.write_int64(1)
        self.assertEqual(writer.bytes, b"\x01\x00\x00\x00\x00\x00\x00\x00")
        writer.write_int64(-1)
        self.assertEqual(
            writer.bytes,
            b"\x01\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff",
        )
        writer.write_int64(-9223372036854775808)
        self.assertEqual(
            writer.bytes,
            b"\x01\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff"
            b"\x00\x00\x00\x00\x00\x00\x00\x80",
        )

    def test_uint64(self) -> None:
        writer = BinaryWriter(ByteOrder.LITTLE)

        writer.write_uint64(1)
        self.assertEqual(writer.bytes, b"\x01\x00\x00\x00\x00\x00\x00\x00")
        writer.write_uint64(18446744073709551615)
        self.assertEqual(
            writer.bytes,
            b"\x01\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff",
        )
        writer.write_uint64(9223372036854775808)
        self.assertEqual(
            writer.bytes,
            b"\x01\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff"
            b"\x00\x00\x00\x00\x00\x00\x00\x80",
        )

    def test_single(self) -> None:
        writer = BinaryWriter(ByteOrder.LITTLE)

        writer.write_single(345.345)
        self.assertEqual(writer.bytes, b"\x29\xAC\xAC\x43")

    def test_double(self) -> None:
        writer = BinaryWriter(ByteOrder.LITTLE)

        writer.write_double(345.345)
        self.assertEqual(writer.bytes, b"\xec\x51\xb8\x1e\x85\x95\x75\x40")

    def test_nullstr(self) -> None:
        writer = BinaryWriter(ByteOrder.LITTLE)

        writer.write_nullstr("Hello")
        self.assertEqual(writer.bytes, b"\x48\x65\x6c\x6c\x6f\x00")

    def test_str(self) -> None:
        writer = BinaryWriter(ByteOrder.LITTLE)

        writer.write_str("Hello")
        self.assertEqual(writer.bytes, b"\x48\x65\x6c\x6c\x6f")

    def test_uint16_big(self) -> None:
        writer = BinaryWriter(ByteOrder.BIG)

        writer.write_uint16(128)
        self.assertEqual(writer.bytes, b"\x00\x80")

    def test_read(self) -> None:
        writer = BinaryWriter(ByteOrder.BIG)

        writer.write(b"\x80")
        self.assertEqual(writer.bytes, b"\x80")
        writer.write(b"\xfa\x00")
        self.assertEqual(writer.bytes, b"\x80\xfa\x00")
