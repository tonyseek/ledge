#!/usr/bin/env python
#-*- coding:utf-8 -*-

from ledge.account import app


@app.route("/")
def home():
    return "@%s.home" % __name__
