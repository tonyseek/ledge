#!/usr/bin/env python
#-*- coding:utf-8 -*-

import collections


navigation_item = collections.namedtuple("NavigationItem", "key label href")
menu_item = collections.namedtuple("MenuItem", "group label href assertion")


class Navigation(object):
    """The navigation context."""

    def __init__(self):
        self.items = []
        self._menu_items = []

    def init_app(self, app):
        """Initialize the application context."""
        app.context_processor(lambda: {'navigation': self})

    def add_item(self, key, label, href):
        """Add a item to the top navigation."""
        self._items.append(navigation_item(key, label, href))

    def add_menu_item(self, group, label, href, assertion=None):
        """Add a item to the context menu."""
        self._menu_items.append(menu_item(group, label, href, assertion))

    @property
    def menu_items(self):
        for item in self._menu_items:
            if item.assertion and item.assertion():
                href = item.href() if callable(item.href) else item.href
                yield menu_item(item.group, item.label, href, None)
