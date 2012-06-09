#!/usr/bin/env python
#-*- coding:utf-8 -*-

from ledge.extensions import db


def signup(user):
    """Sign up a new account."""
    db.session.add(user)
    db.session.commit()
