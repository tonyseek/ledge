#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time
import datetime


def datetime_to_timestamp(then, to_hex=False):
    """Convert a datetime.datetime object to a timestamp with microsecond.

    Example:
    >>> then = datetime.datetime(2012, 11, 10, 15, 38, 4, 35642)
    >>> datetime_to_timestamp(then)
    1352533084035.642
    >>> datetime_to_timestamp(then, to_hex=True)
    '4ce1f26055a3a'
    """
    #: (timestamp + microsecond / 1e6) * 1e3
    timestamp = time.mktime(then.timetuple()) * 1e3 + then.microsecond / 1e3

    #: return the float timestamp value
    if not to_hex:
        return timestamp

    #: convert to integer first, and then convert to hex
    timestamp *= 1e3
    if not timestamp.is_integer():
        raise ValueError("Convert failed and the microsecond is not integer")
    return int_to_hex(int(timestamp))


def timestamp_to_datetime(timestamp, from_hex=False):
    """Convert a timestamp with microsecond to a datetime.datetime object.

    Example:
    >>> timestamp_to_datetime(1352533084035.642)
    datetime.datetime(2012, 11, 10, 15, 38, 4, 35642)
    >>> timestamp_to_datetime("4ce1f26055a3a", from_hex=True)
    datetime.datetime(2012, 11, 10, 15, 38, 4, 35642)
    """
    #: convert to integer first, and then convert to float
    if from_hex:
        timestamp = hex_to_int(timestamp) / 1e3

    return datetime.datetime.fromtimestamp(timestamp / 1e3)


def int_to_hex(integer):
    """Convert a integer to a short hex string.

    Example:
    >>> int_to_hex(8465464864656468)
    '1e134ba21dcc54'
    """
    return hex(integer).rstrip("L").replace("0x", "")


def hex_to_int(hexstr):
    """Convert a hex string to a integer.

    Example:
    >>> hex_to_int("1e134ba21dcc54")
    8465464864656468L
    """
    return int("0x%s" % hexstr, base=16)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
