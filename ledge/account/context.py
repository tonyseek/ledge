#!/usr/bin/env python
#-*- coding:utf-8 -*-

import functools

from flask import g, session, url_for, abort
from flask.ext.babel import gettext as _

from ledge.extensions import acl, identity, db, nav
from ledge.account import app
from ledge.account.models import User, Role


# -----------
# Basic Roles
# -----------

@app.before_app_first_request
def create_basic_roles():
    """Create basic roles and store them into database."""
    everyone = Role.query("everyone", screen_name="builtin:everyone")
    Role.query("actived", [everyone], screen_name="builtin:actived")
    db.session.commit()


# --------------
# Context Loader
# --------------

def current_user():
    """Get the logined user in current session."""
    if not hasattr(g, "current_user"):
        g.current_user = User.query.get(session.get("uid", ""))
    return g.current_user


@app.before_app_request
def reload_current_user():
    """Reload current logined user from session identity."""
    current_user()


@app.before_app_first_request
def reload_all_roles():
    """Reload all roles from database and register it into the ACL."""
    for role in Role.query.all():
        acl.add_role(role.id, [parent.id for parent in role.parents])


@app.before_app_first_request
def init_nav():
    """Initilize the global layout navigation."""
    #: assertion functions
    without_login = lambda: not current_user()
    with_login = lambda: bool(current_user())

    #: set context variable
    nav.get_current_user = current_user
    nav.get_menu_capital = lambda: current_user().nickname \
            if current_user() else _("My Account")

    #: register session menu
    nav.add_menu_items(
        ("session", _("Login"), url_for("account.login"), without_login),
        ("session", _("Sign Up"), url_for("account.signup"), without_login),
        ("session", _("Logout"), url_for("account.logout"), with_login),
        ("resource", _("My Home"),
                url_for("account.person", id=current_user().id), with_login)
    )


@identity.set_roles_loader
def current_roles():
    for role in getattr(current_user(), "roles", []):
        yield role.id


# --------------
# Session Action
# --------------

def session_login(user):
    """Login a user to current session."""
    session['uid'] = user.id
    reload_current_user()


def session_logout():
    """Remove login information of current session."""
    if "uid" in session:
        del session['uid']
    reload_current_user()


def require_login(wrapped):
    """A decorator to give a HTTP 401 to unauthenticated request."""
    def wrapper(*args, **kwargs):
        if not current_user():
            abort(401)
        return wrapped(*args, **kwargs)
    return functools.update_wrapper(wrapper, wrapped)
