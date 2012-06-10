#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import render_template, redirect, url_for, request
from flask.ext.babel import gettext as _

from ledge.corelib.views import as_view, MethodView
from ledge.account import app
from ledge.account.models import User
from ledge.account.services import (SignUpService, TokenUsedError,
        TokenWrongError)
from ledge.account.forms import SignUpForm
from ledge.account.context import session_login


@app.route("/signup")
@as_view("signup")
class SignUpView(MethodView):
    """The view of signing up."""

    def prepare(self):
        self.form = SignUpForm()
        self.user = User()
        self.service = SignUpService(self.user)

    def get(self):
        return render_template("signup.html", **vars(self))

    def post(self):
        #: validate input
        if not self.form.validate():
            return render_template("signup.html", **vars(self))

        #: inject data
        self.form.populate_obj(self.user)

        #: call the sign up service
        self.service.signup()
        self.service.send_confirm_mail()

        #: redirect to user's person page
        return redirect(url_for("account.person", id=self.user.id))


@app.route("/<string:id>/confirm")
def confirm(id):
    """The view of confirm a new signing account's email."""
    #: get resources
    user = User.query.get_or_404(id)
    service = SignUpService(user)
    input_token = request.args['token']

    #: active current account
    try:
        service.active(input_token)
    except TokenUsedError:
        message = _(u"The account had been actived.")
        return render_template("confirm-failed.html", message=message), 403
    except TokenWrongError:
        message = _(u"The active token is invalid.")
        return render_template("confirm-failed.html", message=message), 403

    #: automatic sign in
    session_login(user)

    #: output a success message
    message = _(u"The account has been actived successfully.")
    return render_template("confirm-success.html", message=message)


@app.route("/<string:id>")
def person(id):
    user = User.query.get_or_404(id)
    return render_template("person.html", user=user)
