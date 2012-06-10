#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sqlalchemy import func
from sqlalchemy.ext.hybrid import Comparator, hybrid_property


class LowerIdComparator(Comparator):
    """Reload comparator of id property to be compared in lower-case."""

    def operate(self, op, other):
        """Convert the id to lower-case."""
        return op(func.lower(self.__clause_element__()), func.lower(other))


class LowerIdMixin(object):
    """Let the id property could be compared in lower-case."""

    ID_ATTR = "_id"

    @hybrid_property
    def id(self):
        return unicode(getattr(self, self.ID_ATTR)).lower()

    @id.setter
    def __set_id(self, value):
        self._id = unicode(value).lower()

    @id.comparator
    def __compare_id(cls):
        return LowerIdComparator(getattr(cls, cls.ID_ATTR))
