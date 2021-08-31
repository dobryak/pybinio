import unittest

from binio import BinaryReader, ByteOrder


class BinaryReaderTests(unittest.TestCase):
    def test_size(self) -> None:
        reader = BinaryReader(b"\x01\x00", ByteOrder.LITTLE)

        self.assertEqual(reader.read_bool(), True)

    def test_bytes(self) -> None:
        reader = BinaryReader(b"\x01\x00\xff", ByteOrder.LITTLE)

        self.assertEqual(reader.read_bool(), True)
        self.assertEqual(reader.bytes, b"\x01\x00\xff")
        self.assertEqual(reader.read(), b"\x00\xff")

    def test_read_bool(self) -> None:
        reader = BinaryReader(b"\x01\x00", ByteOrder.LITTLE)

        self.assertEqual(reader.read_bool(), True)
        self.assertEqual(reader.read_bool(), False)

    def test_read_uleb128(self) -> None:
        reader = BinaryReader(
            b"\xac\x02\x05\xff\x01\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01",
            ByteOrder.LITTLE,
        )

        self.assertEqual(reader.read_uleb128(), 300)
        self.assertEqual(reader.read_uleb128(), 5)
        self.assertEqual(reader.read_uleb128(), 255)
        self.assertEqual(reader.read_uleb128(), 18446744073709551615)

    def test_read_zigzagint(self) -> None:
        reader = BinaryReader(
            b"\x09\x0a\xb1\x05",
            ByteOrder.LITTLE,
        )

        self.assertEqual(reader.read_zigzagint(), -5)
        self.assertEqual(reader.read_zigzagint(), 5)
        self.assertEqual(reader.read_zigzagint(), -345)

    def test_read_int8(self) -> None:
        reader = BinaryReader(b"\x01\x7f\x80", ByteOrder.LITTLE)

        self.assertEqual(reader.read_int8(), 1)
        self.assertEqual(reader.read_int8(), 127)
        self.assertEqual(reader.read_int8(), -128)

    def test_read_uint8(self) -> None:
        reader = BinaryReader(b"\xff\x00\x80", ByteOrder.LITTLE)

        self.assertEqual(reader.read_uint8(), 255)
        self.assertEqual(reader.read_uint8(), 0)
        self.assertEqual(reader.read_uint8(), 128)

    def test_read_char(self) -> None:
        reader = BinaryReader(b"\x41\x79", ByteOrder.LITTLE)

        self.assertEqual(reader.read_char(), "A")
        self.assertEqual(reader.read_char(), "y")

    def test_read_int16(self) -> None:
        reader = BinaryReader(b"\x01\x00\xff\xff\x00\x80", ByteOrder.LITTLE)

        self.assertEqual(reader.read_int16(), 1)
        self.assertEqual(reader.read_int16(), -1)
        self.assertEqual(reader.read_int16(), -32768)

    def test_read_uint16(self) -> None:
        reader = BinaryReader(b"\x01\x00\xff\xff\x00\x80", ByteOrder.LITTLE)

        self.assertEqual(reader.read_uint16(), 1)
        self.assertEqual(reader.read_uint16(), 65535)
        self.assertEqual(reader.read_uint16(), 32768)

    def test_read_int32(self) -> None:
        reader = BinaryReader(
            b"\x01\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x80", ByteOrder.LITTLE
        )

        self.assertEqual(reader.read_int32(), 1)
        self.assertEqual(reader.read_int32(), -1)
        self.assertEqual(reader.read_int32(), -2147483648)

    def test_read_uint32(self) -> None:
        reader = BinaryReader(
            b"\x01\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x80", ByteOrder.LITTLE
        )

        self.assertEqual(reader.read_uint32(), 1)
        self.assertEqual(reader.read_uint32(), 4294967295)
        self.assertEqual(reader.read_uint32(), 2147483648)

    def test_read_int64(self) -> None:
        reader = BinaryReader(
            b"\x01\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff"
            b"\x00\x00\x00\x00\x00\x00\x00\x80",
            ByteOrder.LITTLE,
        )

        self.assertEqual(reader.read_int64(), 1)
        self.assertEqual(reader.read_int64(), -1)
        self.assertEqual(reader.read_int64(), -9223372036854775808)

    def test_read_uint64(self) -> None:
        reader = BinaryReader(
            b"\x01\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff"
            b"\x00\x00\x00\x00\x00\x00\x00\x80",
            ByteOrder.LITTLE,
        )

        self.assertEqual(reader.read_uint64(), 1)
        self.assertEqual(reader.read_uint64(), 18446744073709551615)
        self.assertEqual(reader.read_uint64(), 9223372036854775808)

    def test_read_single(self) -> None:
        reader = BinaryReader(
            b"\x29\xAC\xAC\x43",
            ByteOrder.LITTLE,
        )

        self.assertAlmostEqual(reader.read_single(), 345.345, 5)

    def test_read_double(self) -> None:
        reader = BinaryReader(
            b"\xec\x51\xb8\x1e\x85\x95\x75\x40",
            ByteOrder.LITTLE,
        )

        self.assertAlmostEqual(reader.read_double(), 345.345, 5)

    def test_read_nullstr(self) -> None:
        reader = BinaryReader(
            b"\x48\x65\x6c\x6c\x6f\x00",
            ByteOrder.LITTLE,
        )

        self.assertEqual(reader.read_nullstr(), "Hello")

    def test_read_str(self) -> None:
        reader = BinaryReader(
            b"\x48\x65\x6c\x6c\x6f",
            ByteOrder.LITTLE,
        )

        self.assertEqual(reader.read_str(5), "Hello")

    def test_read_uint16_big(self) -> None:
        reader = BinaryReader(b"\x00\x80", ByteOrder.BIG)

        self.assertEqual(reader.read_uint16(), 128)

    def test_read(self) -> None:
        reader = BinaryReader(b"\xfa\x00\x80", ByteOrder.LITTLE)

        self.assertEqual(reader.read(2), b"\xfa\x00")
        self.assertEqual(reader.read(), b"\x80")
