#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import render_template, redirect, url_for

from ledge.corelib.views import as_view, MethodView
from ledge.account import app
from ledge.account.models import User
from ledge.account.services import signup
from ledge.account.forms import SignUpForm


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
