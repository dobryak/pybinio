"""
:mod:`binio.enums` defines enumerators

"""

from enum import IntEnum, auto

__all__ = ["ByteOrder"]


class ByteOrder(IntEnum):
    MACHINE = auto()
    BIG = auto()
    LITTLE = auto()
