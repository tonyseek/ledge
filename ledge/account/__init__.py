#!/usr/bin/env python
#-*- coding:utf-8 -*-

import flask


__all__ = ("app", "views", "models", "services")

app = flask.Blueprint("account", __name__,
        template_folder="templates",
        static_folder="static",
        url_prefix="")
