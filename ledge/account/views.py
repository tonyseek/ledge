#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import render_template, redirect, url_for
from flask.ext.wtf import (Form, TextField, PasswordField, RadioField,
        SubmitField, ValidationError, required, email)
from flask.ext.wtf.html5 import EmailField

from ledge.corelib.views import as_view, MethodView
from ledge.account import app
from ledge.account.models import User
from ledge.account.services import signup


class SignUpForm(Form):
    """The form of signing up."""

    def id_unique(self, id):
        if User.query.get(id.data):
            raise ValidationError("The %s has been used." % id.label.text)

    def email_unique(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("The %s has been used." % email.label.text)

    GENDER_CHOICES = [(gender, gender.title()) for gender in User.GENDER_ENUM]

    id = TextField("User Name", [required(), id_unique])
    email = EmailField("Email", [required(), email(), email_unique])
    password = PasswordField("Password", [required()])
    gender = RadioField("Gender", [required()], choices=GENDER_CHOICES)
    nickname = TextField("Screen Name", [])
    submit = SubmitField("Sign Up")


@app.route("/signup")
@as_view("signup")
class SignUpView(MethodView):
    """The view of signing up."""

    def prepare(self):
        self.form = SignUpForm()

    def get(self):
        return render_template("signup.html", **vars(self))

    def post(self):
        if not self.form.validate():
            return render_template("signup.html", **vars(self))
        user = User()
        self.form.populate_obj(user)
        signup(user)
        return redirect(url_for("account.signup"))


@app.route("/people/<string:id>")
def profile(id):
    user = User.query.get_or_404(id)
    return render_template("profile.html", user=user)
