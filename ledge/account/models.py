#!/usr/bin/env python
#-*- coding:utf-8 -*-

import uuid
import hashlib
import datetime

from ledge.extensions import db
from ledge.corelib.jsonize import JsonizableMixin


current_datetime = lambda: datetime.datetime.utcnow()


class UserQuery(db.Query):
    """Query Handler of `User` model."""

    def get(self, id):
        return super(UserQuery, self).get(id.lower())

    def authenticate(self, email_or_username, password):
        """Authenicate by email/username and password.

        If email/username isn't exist or password is wrong, this method would
        return `None`, otherwise return the `models.User` model.
        """
        condition = ((User.email == email_or_username.lower()) |
                     (User.username == email_or_username))
        user = self.filter(condition).first()
        if not user:
            raise UserNotFound
        if user.check_password(password):
            raise PasswordWrong
        return user


class User(JsonizableMixin, db.Model):
    """The account of the user."""

    query_class = UserQuery
    JSONIZE_ATTRS = ("id", "nickname", "gender", "created")
    GENDER_ENUM = ("male", "female", "unknown")

    id = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(64), unique=True)
    nickname = db.Column(db.Unicode(20))
    gender = db.Column(db.Enum(name="gender", *GENDER_ENUM), default="unknown")
    salt = db.Column(db.String(32), nullable=False)
    hashed_password = db.Column(db.String(64), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=current_datetime)

    def __init__(self, **data):
        password = data.pop("password", "")
        super(User, self).__init__(**data)
        self.change_password(password)
        self.nickname = self.nickname or self.id

    def __repr__(self):
        return "<User %s(%s)>" % (self.id, self.email)

    def change_password(self, password):
        """Change a new password."""
        self.salt = uuid.uuid4().hex
        self.hashed_password = self._hash_password(self.salt, password)

    def check_password(self, input_password):
        """Check the input password is right or wrong."""
        input_password = self._hash_password(self.salt, input_password)
        return input_password == self.hashed_password

    @staticmethod
    def _hash_password(salt, password):
        """Calculate the hashed value of password."""
        hashed = hashlib.sha256()
        hashed.update("<%s|%s>" % (salt, password))
        return hashed.hexdigest()

    @db.validates("id")
    def validate_id(self, key, value):
        return value.lower()


class Role(db.Model):
    """The role of the user."""

    id = db.Column(db.String(20), primary_key=True)
    parent_id = db.Column(db.ForeignKey(id))
    screen_name = db.Column(db.Unicode(20))


# ----------
# Exceptions
# ----------

class UserNotFound(Exception):
    pass


class PasswordWrong(Exception):
    pass
