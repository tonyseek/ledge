#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask.ext.wtf import TextField, PasswordField, RadioField, SubmitField
from flask.ext.wtf import required, email
from flask.ext.wtf.html5 import EmailField

from ledge.corelib.forms import Form, unique
from ledge.account.models import User


class SignUpForm(Form):
    """The form of signing up."""

    GENDER_CHOICES = [(gender, gender.title()) for gender in User.GENDER_ENUM]

    id = TextField("User Name", [required(), unique(User.id)])
    email = EmailField("Email", [required(), email(), unique(User.email)])
    password = PasswordField("Password", [required()])
    gender = RadioField("Gender", [required()], choices=GENDER_CHOICES)
    nickname = TextField("Screen Name", [])
    submit = SubmitField("Sign Up")
