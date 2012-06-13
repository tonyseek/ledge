#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Blueprint


__all__ = ("app", "views", "forms", "models", "assets")

app = Blueprint("note", __name__, template_folder="templates",
        static_folder="static", url_prefix="")
