#!/usr/bin/env python
#-*- coding:utf-8 -*-

import itertools

from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.assets import Environment, ManageAssets
from flask.ext.script import prompt_bool
from rbac.acl import Registry
from rbac.proxy import RegistryProxy
from rbac.context import IdentityContext

import ledge.assets


db = SQLAlchemy()
babel = Babel()
mail = Mail()
assets = Environment()
acl = RegistryProxy(Registry())
identity = IdentityContext(acl)


def configure_extensions(app):
    """Initialize and configure all extension to a application instance."""
    db.init_app(app)
    babel.init_app(app)
    mail.init_app(app)
    assets.init_app(app)
    ledge.assets.install(assets)

    @babel.localeselector
    def get_locale():
        accept_languages = app.config.get("ACCEPT_LANGUAGES", ["zh", "en"])
        return request.accept_languages.best_match(accept_languages)

    @app.context_processor
    def assets_variables():
        get_namespace = lambda name: name.split(".", 1)[0]
        named_assets = itertools.groupby(assets._named_bundles, get_namespace)
        return {'assets': {k: sorted(v) for k, v in named_assets}}


def configure_manager(manager):
    manager.add_command("assets", ManageAssets(assets))

    @manager.command
    def create_db():
        """Creates tables in the database with existed schema."""
        db.create_all()

    @manager.command
    def drop_db():
        """Drop all tables in the database."""
        if prompt_bool("Confirm to drop all table from database"):
            db.drop_all()
