#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages


metadata = {'name': "ledge",
            'version': "0.1",
            'description': "A online utility to manage and share knownledge",
            'keywords': "knownledge",
            'author': "TonySeek",
            'author_email': "tonyseek@gmail.com",
            'license': "MIT License",
            'packages': find_packages(),
            'zip_safe': False,
            'platforms': "any",
            'test_suite': "tests.run_tests"}

if __name__ == "__main__":
    setup(**metadata)
