#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import itertools

import flask

from ledge.extensions import configure_extensions
from ledge.logging import make_file_handler


class Application(flask.Flask):
    """The web application named ledge."""

    CONFIG_ENV = "LEDGE_CONFIG"
    LOG_FILE = "../app.log"

    BUILTIN_BLUEPRINTS = ["ledge.account.app"]

    def __init__(self, import_name=__package__, *args, **kwargs):
        super(Application, self).__init__(import_name, *args, **kwargs)
        self.config.from_envvar(self.CONFIG_ENV)
        self._init_extensions()
        self._init_logging()
        self._init_blueprints()

    def _init_extensions(self):
        """Initialize the extensions and plugins of the application."""
        configure_extensions(self)

    def _init_logging(self):
        """Create a default logger."""
        self.config.setdefault("LOG_FILE", self.get_full_path(self.LOG_FILE))
        file_handler = make_file_handler(self.config["LOG_FILE"])
        self.logger.addHandler(file_handler)

    def _init_blueprints(self):
        """Register the built-in blueprints of the application."""
        self.config.setdefault("BLUEPRINTS", [])

        builtins = self.BUILTIN_BLUEPRINTS
        others = self.config["BLUEPRINTS"]

        for name in itertools.chain(builtins, others):
            self.register_blueprint_by_name(name)

    def register_blueprint_by_name(self, name):
        """Register the blueprint by its name."""
        # split the name
        splited = name.split(".")
        blueprint_name = splited[-1]
        module_name = ".".join(splited[:-1])
        package_name = splited[0]
        # dynamic find the blueprint
        module = __import__(module_name, fromlist=[package_name])
        blueprint = getattr(module, blueprint_name)
        # load the all submodules
        for submodule_name in getattr(module, "__all__", []):
            if not hasattr(module, submodule_name):
                __import__("%s.%s" % (module_name, submodule_name))
        # register it
        self.register_blueprint(blueprint)
        self.logger.info("Loaded %r" % name)

    def get_full_path(self, relative_path):
        """Create a absolute path from a relative path.

        Example:
            >>> app.root_path
            '/home/tonyseek/projects/ledge/ledge'
            >>> app.get_full_path("../somefile")
            '/home/tonyseek/projects/ledge/somefile'
        """
        path = os.path.join(self.root_path, relative_path)
        return os.path.abspath(path)
