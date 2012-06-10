#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask.ext.wtf import TextField, PasswordField, RadioField, SubmitField
from flask.ext.wtf import required, email
from flask.ext.wtf.html5 import EmailField
from flask.ext.babel import lazy_gettext as _

from ledge.corelib.forms import Form, unique
from ledge.account.models import User


class SignUpForm(Form):
    """The form of signing up."""

    GENDER_CHOICES = [
            ("unknown", _(u"Private")),
            ("male", _(u"Male")),
            ("female", _(u"Female"))]

    id = TextField(_("User Name"), [required(), unique(User, User.id)])
    email = EmailField(_("Email"), [required(), email(),
            unique(User, User.email)])
    password = PasswordField(_("Password"), [required()])
    gender = RadioField(_("Gender"), [required()],
            choices=GENDER_CHOICES, default="unknown")
    nickname = TextField(_("Screen Name"), [])
    submit = SubmitField(_("Sign Up"))
