#!/usr/bin/env python
#-*- coding:utf-8 -*-

import flask.views


def as_view(name=None):
    """A decorator to call the `as_view` method of class based view.

    Example:

    >>> @app.route("/posts/<int:id>")
    ... @as_view(name="post")
    ... class PostView(flask.view.MethodView):
    ...
    ...     def get(self, id):
    ...         return flask.render_template("post.html", id=id)
    """
    return lambda view_class: view_class.as_view(name)


class MethodView(flask.views.MethodView):

    def prepare(self, *args, **kwargs):
        pass

    def after(self, rv):
        return rv

    def dispatch_request(self, *args, **kwargs):
        self.prepare(*args, **kwargs)
        rv = super(MethodView, self).dispatch_request()
        return self.after(rv)
