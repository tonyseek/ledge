#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask.ext.assets import Bundle


jquery = Bundle("libs/jquery-1.7.2.js",
        output="packed/jquery.packed.js", filters="jsmin")
bootstrap = Bundle("libs/bootstrap/css/bootstrap.css",
        "libs/bootstrap/css/bootstrap-responsive.css",
        output="packed/bootstrap.packed.css")
bootstrap_plugins = Bundle("libs/bootstrap/js/bootstrap.js",
        output="packed/bootstrap.packed.js")


def install(assets):
    assets.register('scripts.!jquery', jquery)
    assets.register('scripts.bootstrap', bootstrap_plugins)
    assets.register('stylesheets.bootstrap', bootstrap)
