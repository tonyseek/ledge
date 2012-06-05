#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel
from flask.ext.mail import Mail


db = SQLAlchemy()
babel = Babel()
mail = Mail()


def configure_extensions(app):
    """Initialize and configure all extension to a application instance."""
    db.init_app(app)
    babel.init_app(app)
    mail.init_app(app)
