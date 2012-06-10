#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import render_template, redirect, url_for, request, flash
from flask.ext.babel import gettext as _

from ledge.corelib.views import as_view, MethodView
from ledge.account import app
from ledge.account.models import User, UserNotFoundError, PasswordWrongError
from ledge.account.services import (SignUpService, TokenUsedError,
        TokenWrongError)
from ledge.account.forms import SignUpForm, LoginForm
from ledge.account.context import session_login, session_logout, require_login


# -------------
# Sign Up Views
# -------------

@app.route("/signup")
@as_view(name="signup")
class SignUpView(MethodView):
    """The view to sign up."""

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
    """The view to confirm a new account's email."""
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


# -----------
# Login Views
# -----------

@app.route("/login")
@as_view(name="login")
class LoginView(MethodView):
    """The view to login."""

    def prepare(self):
        self.form = LoginForm()

    def _render_page(self):
        return render_template("login.html", **vars(self))

    def get(self):
        return self._render_page()

    def post(self):
        #: validate input
        if not self.form.validate():
            return self._render_page()

        #: try to authenticate
        try:
            user = User.query.authenticate(self.form.login.data,
                    self.form.password.data)
        except (UserNotFoundError, PasswordWrongError):
            message = _(u"The user is not found or the password is wrong.")
            flash(message, "error")
            return self._render_page()
        else:
            session_login(user)
            flash(_(u"Welcome %(name)s.", name=user.nickname), "info")

        #: redirect to user's person page
        return redirect(url_for("master.home"))


@app.route("/logout")
@require_login
def logout():
    session_logout()
    return redirect(url_for("master.home"))


@app.route("/<string:id>")
def person(id):
    user = User.query.get_or_404(id)
    return render_template("person.html", user=user)
