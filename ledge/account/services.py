#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import render_template
from flask.ext.mail import Message
from flask.ext.babel import gettext as _

from ledge.corelib.config import get_notify_address
from ledge.extensions import db, mail
from ledge.account.models import Role, ActiveToken


class SignUpService(object):
    """The work flow of signing up."""

    def __init__(self, user):
        self.user = user

    def signup(self):
        """Sign up a new account."""
        #: assign a new active token
        self.user.active_token = ActiveToken()

        #: store into database
        db.session.add(self.user)
        db.session.commit()

    def send_confirm_mail(self):
        """Send confirm mail to active user."""
        message = Message(_("Email Confirm: Active Your Account"),
                sender=get_notify_address(), recipients=[self.user.email])
        message.html = render_template("confirm-email.html", user=self.user)
        mail.send(message)

    def active(self, input_token):
        """Confirm to active user with the secret token."""
        #: while the user is actived
        if not self.user.active_token:
            raise TokenUsedError
        #: while the token is wrong
        if self.user.active_token.value != input_token:
            raise TokenWrongError

        #: active the user and delete the used token
        self.user.roles.append(Role.query("actived"))
        db.session.delete(self.user.active_token)
        db.session.commit()


# ---------
# Exception
# ---------

class TokenUsedError(Exception):
    """The user has been actived (the token has been used)."""


class TokenWrongError(Exception):
    """The active token is not existed or wrong."""
