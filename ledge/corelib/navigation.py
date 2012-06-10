#!/usr/bin/env python
#-*- coding:utf-8 -*-


class Navigation(object):
    """The navigation context."""

    def __init__(self, app=None):
        self.app = None
        self.navs = []
        self.menus = []
        self.get_current_user = None
        self.get_menu_capital = None

        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the application context."""
        self.app = app

        @app.context_processor
        def layout_template_context():
            return {'nav': vars(self)}

    def add_nav_item(self, key, label, href):
        """Add a item to top navigation."""
        self.navs.append((key, label, href))

    def add_nav_items(self, *items):
        """Add many items to top navigation."""
        for item in items:
            self.add_nav_item(*item)

    def add_menu_item(self, group, label, href, assertion=None):
        """Add a item to right menu."""
        self.menus.append({'group': group, 'item': (label, href, assertion)})

    def add_menu_items(self, *items):
        """Add many items to right menu."""
        for item in items:
            self.add_menu_item(*item)
