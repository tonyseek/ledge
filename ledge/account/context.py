#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import g, session

from ledge.extensions import acl, identity, db
from ledge.account import app
from ledge.account.models import User, Role


# -----------
# Basic Roles
# -----------

@app.before_app_first_request
def create_basic_roles():
    everyone = Role.query("everyone", screen_name="builtin:everyone")
    Role.query("actived", [everyone], screen_name="builtin:actived")
    db.session.commit()


# --------------
# Context Loader
# --------------

@app.before_app_request
def load_current_user():
    g.current_user = User.query.get(session.get("uid", ""))


@app.before_app_first_request
def init_roles():
    for role in Role.query.all():
        acl.add_role(role.id, [parent.id for parent in role.parents])


@identity.set_roles_loader
def load_current_roles():
    for role in getattr(g.current_user, "roles", []):
        yield role.id


# --------------
# Session Action
# --------------

def session_login(user):
    """Login a user to current session."""
    session['uid'] = user.id
    load_current_user()


def session_logout():
    """Remove login information of current session."""
    if "uid" in session:
        del session['uid']
    if hasattr(g, "current_user"):
        del g.current_user
