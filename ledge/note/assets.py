#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask.ext.assets import Bundle

from ledge.extensions import assets


stylesheets_note = Bundle("note/stylesheets/topic.css",
        output="packed/note.packed.css")

assets.register('stylesheets.note', stylesheets_note)
