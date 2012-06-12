#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""JSON Serialize Mixin.

This is a useful utility to extend a class, let it could be serialized.
It's not the same as pickle, but dump a model into a dictionary, which could
be encoded to JSON format.
"""

import datetime


base_types = (type(None), basestring, int, float, list, dict)
type_converters = {}
jsonizable_classes = set()


def register_type_converter(from_type):
    """A decorator to add a type converter for json serialize.

    Example:
        >>> from datetime import datetime
        >>> from time import mktime
        >>>
        >>> @register_type_converter(from_type=datetime)
        ... def datetime_to_timestamp(val):
        ...     return mktime(val.timetuple())
        >>>
    """
    def decorator(converter):
        type_converters[from_type] = converter
        return converter
    return decorator


class Jsonizable(object):
    """Implement to_json method to a model.

    While including this mix-in class, the subject class should implement the
    `JSONIZE_ATTRS` class attribute, it defined which attributes will
    be serialized.

    Example:
        >>> class MyModel(Jsonizable, Base):
        ...     JSONIZE_ATTRS = ["name", "age"]
        ...
        ...     def __init__(self, name, age):
        ...         self.name = name
        ...         self.age = age
        >>>
        >>> my_model = MyModel("spam", 2010)
        >>> my_model.to_json()
        {'age': 2010, 'name': 'spam'}
        >>>
        >>> import json
        >>> json.dumps(my_model.to_json())
        '{"age": 2010, "name": "spam"}'
        >>>
    """

    def to_json(self):
        """Generate a dictionary for json serialize."""
        # update the subclasses set
        jsonizable_classes.update(Jsonizable.__subclasses__())
        # serialize to dictionary
        serialized = {}
        for attr in self.JSONIZE_ATTRS:
            value = vars(self)[attr]
            while not isinstance(value, base_types):
                value_type = type(value)
                if value_type in type_converters:
                    value = type_converters[value_type](value)
                elif value_type in jsonizable_classes:
                    value = value.to_json()
                else:
                    raise ValueError("Could not convert %r" % value_type)
            serialized[attr] = value
        return serialized


# -----------------------
# Builtin Type Converters
# -----------------------

@register_type_converter(datetime.datetime)
def datetime_to_string(value):
    """Convert a datetime.datetime object to ISO format string."""
    return value.isoformat()
