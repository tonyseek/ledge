#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys

from flask.ext.script import Manager
from pep8 import _main as check_pep8

from ledge.application import Application
from ledge.extensions import configure_manager


app = Application()
manager = Manager(app)
configure_manager(manager)


@manager.option('-i', dest='input_file', help="check the input file.")
def pep8(input_file=None):
    """Checks the project's coding style by PEP 8."""
    sys.argv = ["--statistics", "--count", input_file or app.root_path]
    check_pep8()


if __name__ == "__main__":
    manager.run()
