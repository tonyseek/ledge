#!/usr/bin/env python
#-*- coding:utf-8 -*-

import urlparse

from flask import current_app, request


def get_notify_address():
    url_root = urlparse.urlparse(request.url_root)
    current_app.config.setdefault("NOTIFY_ADDRESS",
            "no-reply@{0}".format(url_root.netloc))
    return current_app.config['NOTIFY_ADDRESS']
