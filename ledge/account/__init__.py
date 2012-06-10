#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Blueprint


__all__ = ("app", "views", "models", "services", "forms", "db", "context")

app = Blueprint("account", __name__, template_folder="templates",
        static_folder="static", url_prefix="/account")
