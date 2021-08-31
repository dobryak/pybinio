"""
:mod:`binio.exceptions` defines the following exception hierarchy:

* :exc: `BinIOException`
    * :exc: ``

"""

__all__ = [
    "BinIOException",
    "NotEnoughBytes",
]


class BinIOException(Exception):
    """
    Base class for all :mod:`binio` exceptions.
    """


class NotEnoughBytes(BinIOException):
    """
    Raised when there is no enought bytes in the
    underlying buffer for processing.

    """


class OutOfRange(BinIOException):
    """
    Raised when the given value is too big to be packed
    to the requested format.

    """
