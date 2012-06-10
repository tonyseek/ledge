#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Blueprint


__all__ = ("app", "views")

app = Blueprint("master", __name__, template_folder="templates",
        static_folder="static", url_prefix="")
