#!/usr/bin/env python
#-*- coding:utf-8 -*-

import uuid
import hashlib
import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from ledge.extensions import db
from ledge.corelib.mixins.jsonize import Jsonizable
from ledge.account.db import LowerIdMixin


current_datetime = lambda: datetime.datetime.utcnow()


# ---------
# User Role
# ---------

class UserRole(db.Model):
    """The middle table for users having roles."""

    user_id = db.Column(db.ForeignKey("user.id"), primary_key=True)
    role_id = db.Column(db.ForeignKey("role.id"), primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=current_datetime)


class RoleClosure(db.Model):
    """The role's inheritance relationship to itself."""

    parent_id = db.Column(db.ForeignKey("role.id"), primary_key=True)
    child_id = db.Column(db.ForeignKey("role.id"), primary_key=True)


class RoleQuery(db.Query):
    """Query Handler for `Role` model."""

    def create(self, role_id, parents=[], screen_name=None):
        role = Role(id=role_id, parents=list(parents),
                screen_name=screen_name)
        db.session.add(role)
        return role

    def __call__(self, role_id, *args, **kwargs):
        return self.get(role_id) or self.create(role_id, *args, **kwargs)


class Role(LowerIdMixin, db.Model):
    """The role of the user."""

    query_class = RoleQuery
    primary_key = db.Column("id", db.String(20), primary_key=True)
    parents = db.relationship("Role", secondary=RoleClosure.__table__,
            primaryjoin=(RoleClosure.child_id == primary_key),
            secondaryjoin=(RoleClosure.parent_id == primary_key))
    screen_name = db.Column(db.Unicode(20))

    def __unicode__(self):
        return self.screen_name or self.id

    def __eq__(self, other):
        return hasattr(other, "id") and self.id == other.id

    def __hash__(self):
        return hash(self.id)


# ------------
# User Account
# ------------

class UserQuery(db.Query):
    """Query Handler of `User` model."""

    def authenticate(self, email_or_username, password):
        """Authenicate by email/username and password.

        If email/username isn't exist or password is wrong, this method would
        return `None`, otherwise return the `models.User` model.
        """
        condition = ((User.email == email_or_username) |
                     (User.id == email_or_username))
        user = self.filter(condition).first()
        if not user:
            raise UserNotFoundError
        if not user.check_password(password):
            raise PasswordWrongError
        return user


class User(Jsonizable, LowerIdMixin, db.Model):
    """The account of the user."""

    query_class = UserQuery
    JSONIZE_ATTRS = ("id", "nickname", "gender", "created")
    GENDER_ENUM = ("male", "female", "unknown")

    primary_key = db.Column("id", db.String(20), primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    nickname = db.Column(db.Unicode(20))
    gender = db.Column(db.Enum(name="gender", *GENDER_ENUM), nullable=False)
    salt = db.Column(db.String(32), nullable=False)
    hashed_password = db.Column(db.String(64), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=current_datetime)
    roles = db.relationship(Role, secondary=UserRole.__table__)

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

    password = hybrid_property(lambda self: None, change_password)

    @staticmethod
    def _hash_password(salt, password):
        """Calculate the hashed value of password."""
        hashed = hashlib.sha256()
        hashed.update("<%s|%s>" % (salt, password))
        return hashed.hexdigest()


class ActiveToken(db.Model):
    """The active token of new account."""

    user_id = db.Column(db.ForeignKey(User.id), primary_key=True)
    user = db.relationship(User, lazy="joined", uselist=False,
            backref=db.backref("active_token", lazy="select", uselist=False))
    value = db.Column(db.String(32), nullable=False,
            default=lambda: uuid.uuid4().hex)


# ----------
# Exceptions
# ----------

class UserNotFoundError(Exception):
    pass


class PasswordWrongError(Exception):
    pass
