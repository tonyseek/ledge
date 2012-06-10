#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import render_template

from ledge.master import app


@app.route("/")
def home():
    return render_template("home.html")
