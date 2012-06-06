#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import render_template, jsonify
from flask.views import MethodView
from flask.ext.wtf import (Form, TextField, PasswordField, RadioField,
        SubmitField, ValidationError, required, email)
from flask.ext.wtf.html5 import EmailField

from ledge.corelib.decorators import as_view
from ledge.extensions import db
from ledge.account import app
from ledge.account.models import User


class SignUpForm(Form):
    """The form of signing up."""

    def id_unique(self, id):
        label = self.id.label.text.lower()
        if User.query.get(id.data):
            raise ValidationError("The %s has been used." % label)

    GENDER_CHOICES = [(gender, gender.title()) for gender in User.GENDER_ENUM]

    id = TextField("User Name", [required(), id_unique])
    email = EmailField("Email", [required(), email()])
    password = PasswordField("Password", [required()])
    gender = RadioField("Gender", [required()], choices=GENDER_CHOICES)
    nickname = TextField("Screen Name", [])
    submit = SubmitField("Sign Up")


@app.route("/signup")
@as_view("signup")
class SignUpView(MethodView):
    """The view of signing up."""

    def dispatch_request(self):
        self.form = SignUpForm()
        return super(SignUpView.view_class, self).dispatch_request()

    def get(self):
        return render_template("signup.html", **vars(self))

    def post(self):
        if not self.form.validate():
            return jsonify(errors=self.form.errors, id=self.form.id.data)
        user = User()
        self.form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return render_template("signup.html", **vars(self))
